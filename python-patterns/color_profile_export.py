#!/usr/bin/env python3
"""
NEONpulseTechshop Color Profile Export Module
Export calibration results as ICC/ICM profiles
"""

import struct
import datetime
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import os

class ICCProfile:
    """ICC Profile generator for display calibration"""
    
    def __init__(self, display_name: str = "NEONpulseTechshop Calibrated Display"):
        self.display_name = display_name
        self.creation_date = datetime.datetime.now()
        
        # Profile data
        self.white_point = {'x': 0.3127, 'y': 0.3290}  # D65 default
        self.black_point = {'Y': 0.0}
        self.gamma = 2.2
        self.primaries = {
            'red': {'x': 0.640, 'y': 0.330},    # sRGB defaults
            'green': {'x': 0.300, 'y': 0.600},
            'blue': {'x': 0.150, 'y': 0.060}
        }
        self.luminance = 100.0  # cd/m²
        
        # Measurement data
        self.measurements = []
        
    def set_gamma(self, gamma: float):
        """Set display gamma value"""
        self.gamma = gamma
        
    def set_white_point(self, x: float, y: float, Y: float = 1.0):
        """Set white point chromaticity"""
        self.white_point = {'x': x, 'y': y, 'Y': Y}
        
    def set_black_point(self, Y: float):
        """Set black point luminance"""
        self.black_point = {'Y': Y}
        
    def set_primaries(self, red: Dict, green: Dict, blue: Dict):
        """Set RGB primaries"""
        self.primaries = {
            'red': red,
            'green': green,
            'blue': blue
        }
        
    def set_luminance(self, luminance: float):
        """Set peak luminance in cd/m²"""
        self.luminance = luminance
        
    def add_measurement(self, rgb_in: Tuple[int, int, int], 
                       xyz_out: Tuple[float, float, float]):
        """Add calibration measurement point"""
        self.measurements.append({
            'input': rgb_in,
            'output': xyz_out
        })
        
    def calculate_tone_curve(self) -> List[int]:
        """Calculate tone reproduction curve from measurements"""
        if not self.measurements:
            # Use gamma curve if no measurements
            curve = []
            for i in range(256):
                normalized = i / 255.0
                output = pow(normalized, self.gamma)
                curve.append(int(output * 65535))
            return curve
            
        # Interpolate from measurements
        # Group by channel
        channels = {'r': [], 'g': [], 'b': []}
        
        for measurement in self.measurements:
            rgb = measurement['input']
            xyz = measurement['output']
            
            # Simplified - in reality would use proper color math
            channels['r'].append((rgb[0], xyz[0]))
            channels['g'].append((rgb[1], xyz[1]))
            channels['b'].append((rgb[2], xyz[2]))
            
        # Build curves
        curves = []
        for channel in ['r', 'g', 'b']:
            points = sorted(channels[channel])
            curve = self._interpolate_curve(points)
            curves.append(curve)
            
        return curves
        
    def _interpolate_curve(self, points: List[Tuple]) -> List[int]:
        """Interpolate tone curve from measurement points"""
        curve = []
        
        for i in range(256):
            # Find surrounding points
            value = i
            
            # Simple linear interpolation
            lower = None
            upper = None
            
            for x, y in points:
                if x <= value:
                    lower = (x, y)
                if x >= value and upper is None:
                    upper = (x, y)
                    
            if lower and upper and lower[0] != upper[0]:
                # Interpolate
                ratio = (value - lower[0]) / (upper[0] - lower[0])
                output = lower[1] + ratio * (upper[1] - lower[1])
            elif lower:
                output = lower[1]
            elif upper:
                output = upper[1]
            else:
                output = pow(i / 255.0, self.gamma)
                
            curve.append(int(output * 65535))
            
        return curve
        
    def generate_profile(self) -> bytes:
        """Generate ICC profile binary data"""
        # ICC Profile structure (simplified)
        profile = bytearray()
        
        # Header (128 bytes)
        profile.extend(self._create_header())
        
        # Tag table
        tags = self._create_tags()
        profile.extend(self._create_tag_table(tags))
        
        # Tag data
        for tag_data in tags.values():
            profile.extend(tag_data)
            
        return bytes(profile)
        
    def _create_header(self) -> bytes:
        """Create ICC profile header"""
        header = bytearray(128)
        
        # Profile size (will be updated later)
        struct.pack_into('>I', header, 0, 0)
        
        # Preferred CMM type
        header[4:8] = b'NEON'
        
        # Profile version (4.3.0.0)
        struct.pack_into('>I', header, 8, 0x04300000)
        
        # Profile class - display device
        header[12:16] = b'mntr'
        
        # Color space - RGB
        header[16:20] = b'RGB '
        
        # PCS (Profile Connection Space) - XYZ
        header[20:24] = b'XYZ '
        
        # Date and time
        dt = self.creation_date
        struct.pack_into('>H', header, 24, dt.year)
        struct.pack_into('>H', header, 26, dt.month)
        struct.pack_into('>H', header, 28, dt.day)
        struct.pack_into('>H', header, 30, dt.hour)
        struct.pack_into('>H', header, 32, dt.minute)
        struct.pack_into('>H', header, 34, dt.second)
        
        # Profile file signature
        header[36:40] = b'acsp'
        
        # Primary platform
        header[40:44] = b'MSFT'  # Microsoft
        
        # Rendering intent - perceptual
        struct.pack_into('>I', header, 64, 0)
        
        # Illuminant (D65)
        struct.pack_into('>I', header, 68, 0x0000F6D6)  # X
        struct.pack_into('>I', header, 72, 0x00010000)  # Y
        struct.pack_into('>I', header, 76, 0x0000D32D)  # Z
        
        # Creator
        header[80:84] = b'NEON'
        
        return header
        
    def _create_tags(self) -> Dict[str, bytes]:
        """Create all required tags"""
        tags = {}
        
        # Required tags for display profiles
        tags['desc'] = self._create_desc_tag()
        tags['wtpt'] = self._create_xyz_tag(self.white_point)
        tags['bkpt'] = self._create_xyz_tag({'x': 0, 'y': 0, 'Y': self.black_point['Y']})
        tags['rXYZ'] = self._create_xyz_tag(self.primaries['red'])
        tags['gXYZ'] = self._create_xyz_tag(self.primaries['green'])
        tags['bXYZ'] = self._create_xyz_tag(self.primaries['blue'])
        tags['rTRC'] = self._create_curve_tag()
        tags['gTRC'] = self._create_curve_tag()
        tags['bTRC'] = self._create_curve_tag()
        
        # Optional but recommended
        tags['cprt'] = self._create_text_tag("Copyright 2024 NEONpulseTechshop")
        tags['dmnd'] = self._create_text_tag(self.display_name)
        tags['lumi'] = self._create_xyz_tag({'x': 0, 'y': 0, 'Y': self.luminance})
        
        return tags
        
    def _create_tag_table(self, tags: Dict[str, bytes]) -> bytes:
        """Create tag table"""
        table = bytearray()
        
        # Number of tags
        struct.pack_into('>I', table, 0, len(tags))
        table.extend(b'\x00' * (4 - len(table) % 4))  # Padding
        
        # Calculate offsets
        offset = 128 + 4 + len(tags) * 12  # Header + tag count + tag entries
        
        # Tag directory entries
        for signature, data in tags.items():
            # Signature
            table.extend(signature.encode('ascii')[:4].ljust(4))
            # Offset
            struct.pack_into('>I', table, len(table), offset)
            table.extend(b'\x00' * 4)
            # Size
            struct.pack_into('>I', table, len(table), len(data))
            table.extend(b'\x00' * 4)
            
            offset += len(data)
            # Align to 4 bytes
            offset = (offset + 3) & ~3
            
        return table
        
    def _create_desc_tag(self) -> bytes:
        """Create description tag"""
        tag = bytearray()
        
        # Type signature
        tag.extend(b'desc')
        tag.extend(b'\x00' * 4)  # Reserved
        
        # ASCII description
        desc_ascii = self.display_name.encode('ascii')
        struct.pack_into('>I', tag, len(tag), len(desc_ascii) + 1)
        tag.extend(b'\x00' * 4)
        tag.extend(desc_ascii)
        tag.extend(b'\x00')  # Null terminator
        
        # Unicode code
        struct.pack_into('>I', tag, len(tag), 0)
        tag.extend(b'\x00' * 4)
        
        # Unicode count and description
        struct.pack_into('>I', tag, len(tag), 0)
        tag.extend(b'\x00' * 4)
        
        # ScriptCode code and count
        struct.pack_into('>H', tag, len(tag), 0)
        tag.extend(b'\x00' * 2)
        tag.extend(b'\x00')  # Count
        tag.extend(b'\x00' * 67)  # Macintosh description
        
        # Pad to 4-byte boundary
        while len(tag) % 4:
            tag.extend(b'\x00')
            
        return tag
        
    def _create_text_tag(self, text: str) -> bytes:
        """Create text tag"""
        tag = bytearray()
        
        # Type signature
        tag.extend(b'text')
        tag.extend(b'\x00' * 4)  # Reserved
        
        # Text
        tag.extend(text.encode('ascii'))
        tag.extend(b'\x00')  # Null terminator
        
        # Pad to 4-byte boundary
        while len(tag) % 4:
            tag.extend(b'\x00')
            
        return tag
        
    def _create_xyz_tag(self, xyz: Dict) -> bytes:
        """Create XYZ tag"""
        tag = bytearray()
        
        # Type signature
        tag.extend(b'XYZ ')
        tag.extend(b'\x00' * 4)  # Reserved
        
        # Convert xyY to XYZ if needed
        if 'x' in xyz and 'y' in xyz:
            Y = xyz.get('Y', 1.0)
            X = (xyz['x'] / xyz['y']) * Y if xyz['y'] != 0 else 0
            Z = ((1 - xyz['x'] - xyz['y']) / xyz['y']) * Y if xyz['y'] != 0 else 0
        else:
            X = xyz.get('X', 0)
            Y = xyz.get('Y', 0)
            Z = xyz.get('Z', 0)
            
        # Store as s15Fixed16Number (32768 = 1.0)
        struct.pack_into('>I', tag, len(tag), int(X * 0x10000))
        tag.extend(b'\x00' * 4)
        struct.pack_into('>I', tag, len(tag), int(Y * 0x10000))
        tag.extend(b'\x00' * 4)
        struct.pack_into('>I', tag, len(tag), int(Z * 0x10000))
        tag.extend(b'\x00' * 4)
        
        return tag
        
    def _create_curve_tag(self) -> bytes:
        """Create tone curve tag"""
        tag = bytearray()
        
        # Type signature
        tag.extend(b'curv')
        tag.extend(b'\x00' * 4)  # Reserved
        
        # For now, use a simple gamma curve
        # In production, would use measured data
        if self.gamma == 1.0:
            # Linear - count of 0
            struct.pack_into('>I', tag, len(tag), 0)
            tag.extend(b'\x00' * 4)
        else:
            # Gamma curve - 256 points
            struct.pack_into('>I', tag, len(tag), 256)
            tag.extend(b'\x00' * 4)
            
            for i in range(256):
                normalized = i / 255.0
                output = pow(normalized, self.gamma)
                value = int(output * 65535)
                struct.pack_into('>H', tag, len(tag), value)
                tag.extend(b'\x00' * 2)
                
        return tag
        
    def save_profile(self, filename: str):
        """Save ICC profile to file"""
        profile_data = self.generate_profile()
        
        # Update file size in header
        size = len(profile_data)
        profile_data = bytearray(profile_data)
        struct.pack_into('>I', profile_data, 0, size)
        
        # Calculate and update MD5 checksum (optional)
        # For now, leave as zeros
        
        # Write file
        with open(filename, 'wb') as f:
            f.write(profile_data)
            
    def export_json(self, filename: str):
        """Export profile data as JSON for analysis"""
        data = {
            'display_name': self.display_name,
            'creation_date': self.creation_date.isoformat(),
            'white_point': self.white_point,
            'black_point': self.black_point,
            'gamma': self.gamma,
            'primaries': self.primaries,
            'luminance': self.luminance,
            'measurements': self.measurements
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            

class CalibrationReport:
    """Generate calibration reports with before/after comparisons"""
    
    def __init__(self, display_name: str):
        self.display_name = display_name
        self.timestamp = datetime.datetime.now()
        self.before_data = {}
        self.after_data = {}
        self.recommendations = []
        
    def add_before_measurement(self, test_name: str, data: Dict):
        """Add pre-calibration measurement"""
        self.before_data[test_name] = data
        
    def add_after_measurement(self, test_name: str, data: Dict):
        """Add post-calibration measurement"""
        self.after_data[test_name] = data
        
    def analyze_gamma(self):
        """Analyze gamma correction"""
        if 'gamma' in self.before_data and 'gamma' in self.after_data:
            before = self.before_data['gamma']['measured']
            after = self.after_data['gamma']['measured']
            target = self.after_data['gamma']['target']
            
            improvement = abs(target - after) < abs(target - before)
            
            self.recommendations.append({
                'test': 'Gamma',
                'before': before,
                'after': after,
                'target': target,
                'improved': improvement,
                'delta': after - before
            })
            
    def analyze_white_point(self):
        """Analyze white point accuracy"""
        if 'white_point' in self.before_data and 'white_point' in self.after_data:
            before = self.before_data['white_point']
            after = self.after_data['white_point']
            
            # Calculate color temperature
            before_temp = self._xy_to_cct(before['x'], before['y'])
            after_temp = self._xy_to_cct(after['x'], after['y'])
            
            self.recommendations.append({
                'test': 'White Point',
                'before': f"{before_temp}K",
                'after': f"{after_temp}K",
                'target': '6500K',
                'improved': abs(6500 - after_temp) < abs(6500 - before_temp),
                'delta_uv': self._calculate_delta_uv(before, after)
            })
            
    def _xy_to_cct(self, x: float, y: float) -> int:
        """Convert xy chromaticity to color temperature"""
        # Simplified McCamy's formula
        n = (x - 0.3320) / (0.1858 - y)
        cct = 449 * (n ** 3) + 3525 * (n ** 2) + 6823.3 * n + 5520.33
        return int(cct)
        
    def _calculate_delta_uv(self, c1: Dict, c2: Dict) -> float:
        """Calculate color difference in u'v' space"""
        # Convert xy to u'v'
        u1 = 4 * c1['x'] / (-2 * c1['x'] + 12 * c1['y'] + 3)
        v1 = 9 * c1['y'] / (-2 * c1['x'] + 12 * c1['y'] + 3)
        
        u2 = 4 * c2['x'] / (-2 * c2['x'] + 12 * c2['y'] + 3)
        v2 = 9 * c2['y'] / (-2 * c2['x'] + 12 * c2['y'] + 3)
        
        return np.sqrt((u2 - u1) ** 2 + (v2 - v1) ** 2)
        
    def generate_html_report(self, filename: str):
        """Generate HTML calibration report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Calibration Report - {self.display_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #ff00ff, #00ff41);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .section {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        .improved {{
            color: #00ff41;
            font-weight: bold;
        }}
        .degraded {{
            color: #ff00ff;
            font-weight: bold;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #f0f0f0;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>NEONpulseTechshop</h1>
        <h2>Display Calibration Report</h2>
        <p>{self.display_name}</p>
        <p>{self.timestamp.strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>
    
    <div class="section">
        <h3>Calibration Summary</h3>
        <table>
            <tr>
                <th>Test</th>
                <th>Before</th>
                <th>After</th>
                <th>Target</th>
                <th>Result</th>
            </tr>
"""
        
        for rec in self.recommendations:
            status = "improved" if rec['improved'] else "degraded"
            status_text = "✓ Improved" if rec['improved'] else "✗ Degraded"
            
            html += f"""
            <tr>
                <td>{rec['test']}</td>
                <td>{rec['before']}</td>
                <td>{rec['after']}</td>
                <td>{rec['target']}</td>
                <td class="{status}">{status_text}</td>
            </tr>
"""
            
        html += """
        </table>
    </div>
    
    <div class="section">
        <h3>Recommendations</h3>
        <ul>
            <li>Continue to monitor display performance monthly</li>
            <li>Recalibrate if ambient lighting conditions change</li>
            <li>Consider hardware calibration for critical color work</li>
            <li>Save this ICC profile for consistent color across applications</li>
        </ul>
    </div>
    
    <div class="section">
        <h3>Profile Installation</h3>
        <p><strong>Windows:</strong> Right-click the .icm file and select "Install Profile"</p>
        <p><strong>macOS:</strong> Double-click the .icc file to open ColorSync Utility</p>
        <p><strong>Linux:</strong> Copy to ~/.local/share/icc/ or /usr/share/color/icc/</p>
    </div>
</body>
</html>
"""
        
        with open(filename, 'w') as f:
            f.write(html)


def demo_profile_creation():
    """Demonstrate profile creation with sample data"""
    
    # Create profile
    profile = ICCProfile("Demo Monitor - NEONpulseTechshop Calibrated")
    
    # Set measured values
    profile.set_gamma(2.2)
    profile.set_white_point(0.3127, 0.3290)  # D65
    profile.set_luminance(120.0)  # 120 cd/m²
    
    # Set measured primaries (example: sRGB)
    profile.set_primaries(
        red={'x': 0.640, 'y': 0.330},
        green={'x': 0.300, 'y': 0.600},
        blue={'x': 0.150, 'y': 0.060}
    )
    
    # Add some sample measurements
    test_points = [
        (0, 0, 0),
        (64, 64, 64),
        (128, 128, 128),
        (192, 192, 192),
        (255, 255, 255)
    ]
    
    for rgb in test_points:
        # Simulate XYZ measurements
        xyz = (
            rgb[0] / 255.0,
            rgb[1] / 255.0,
            rgb[2] / 255.0
        )
        profile.add_measurement(rgb, xyz)
        
    # Save profile
    profile.save_profile("neonpulse_calibrated.icc")
    profile.export_json("neonpulse_calibration_data.json")
    
    # Create report
    report = CalibrationReport("Demo Monitor")
    
    # Add before/after data
    report.add_before_measurement('gamma', {'measured': 2.8, 'target': 2.2})
    report.add_after_measurement('gamma', {'measured': 2.2, 'target': 2.2})
    
    report.add_before_measurement('white_point', {'x': 0.300, 'y': 0.315})
    report.add_after_measurement('white_point', {'x': 0.3127, 'y': 0.3290})
    
    # Analyze
    report.analyze_gamma()
    report.analyze_white_point()
    
    # Generate report
    report.generate_html_report("calibration_report.html")
    
    print("✓ ICC Profile created: neonpulse_calibrated.icc")
    print("✓ Calibration data exported: neonpulse_calibration_data.json")
    print("✓ Calibration report generated: calibration_report.html")


if __name__ == "__main__":
    demo_profile_creation()