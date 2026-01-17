# iOS Asset Requirements

## App Icon Sizes

iOS requires multiple icon sizes for different devices, contexts, and scale factors. All icons must be placed in an Asset Catalog (`.xcassets`).

### iPhone Icons

| Size (pt) | Scale | Pixels | Usage |
|-----------|-------|--------|-------|
| 20x20 | 2x | 40x40 | Spotlight, Settings (iPhone) |
| 20x20 | 3x | 60x60 | Spotlight, Settings (iPhone) |
| 29x29 | 2x | 58x58 | Settings (iPhone) |
| 29x29 | 3x | 87x87 | Settings (iPhone) |
| 40x40 | 2x | 80x80 | Spotlight (iPhone) |
| 40x40 | 3x | 120x120 | Spotlight (iPhone) |
| 60x60 | 2x | 120x120 | App Icon (iPhone) |
| 60x60 | 3x | 180x180 | App Icon (iPhone) |

### iPad Icons

| Size (pt) | Scale | Pixels | Usage |
|-----------|-------|--------|-------|
| 20x20 | 1x | 20x20 | Spotlight, Settings (iPad) |
| 20x20 | 2x | 40x40 | Spotlight, Settings (iPad) |
| 29x29 | 1x | 29x29 | Settings (iPad) |
| 29x29 | 2x | 58x58 | Settings (iPad) |
| 40x40 | 1x | 40x40 | Spotlight (iPad) |
| 40x40 | 2x | 80x80 | Spotlight (iPad) |
| 76x76 | 1x | 76x76 | App Icon (iPad) |
| 76x76 | 2x | 152x152 | App Icon (iPad) |
| 83.5x83.5 | 2x | 167x167 | App Icon (iPad Pro) |

### App Store Icon
| Size | Pixels | Notes |
|------|--------|-------|
| 1024x1024 | 1024x1024 | Required for App Store submission |

---

## Complete Size Reference (Modern iOS)

Starting with iOS 18 and Xcode 15+, Apple simplified the requirements. A single 1024x1024 icon can be used, with the system generating all other sizes. However, for maximum quality control, provide these key sizes:

### Essential Sizes (Recommended)
| Pixels | Purpose |
|--------|---------|
| 1024x1024 | App Store, source of truth |
| 180x180 | iPhone App Icon (@3x) |
| 167x167 | iPad Pro App Icon (@2x) |
| 152x152 | iPad App Icon (@2x) |
| 120x120 | iPhone App Icon (@2x), Spotlight (@3x) |
| 87x87 | Settings (@3x) |
| 80x80 | Spotlight (@2x) |
| 76x76 | iPad App Icon (@1x) |
| 60x60 | Spotlight iPhone (@3x) |
| 58x58 | Settings (@2x) |
| 40x40 | Spotlight (@1x, @2x) |
| 29x29 | Settings (@1x) |
| 20x20 | Notification (@1x) |

---

## Apple Watch Icons

| Size (pt) | Scale | Pixels | Usage |
|-----------|-------|--------|-------|
| 24x24 | 2x | 48x48 | Notification Center (38mm) |
| 27.5x27.5 | 2x | 55x55 | Notification Center (42mm) |
| 29x29 | 2x | 58x58 | Settings (all watches) |
| 29x29 | 3x | 87x87 | Settings (all watches) |
| 40x40 | 2x | 80x80 | Home Screen (38mm) |
| 44x44 | 2x | 88x88 | Home Screen (40mm) |
| 46x46 | 2x | 92x92 | Home Screen (41mm) |
| 50x50 | 2x | 100x100 | Home Screen (44mm) |
| 51x51 | 2x | 102x102 | Home Screen (45mm) |
| 54x54 | 2x | 108x108 | Home Screen (49mm Ultra) |
| 1024x1024 | 1x | 1024x1024 | App Store |

---

## macOS Icons

| Size (pt) | Scale | Pixels |
|-----------|-------|--------|
| 16x16 | 1x | 16x16 |
| 16x16 | 2x | 32x32 |
| 32x32 | 1x | 32x32 |
| 32x32 | 2x | 64x64 |
| 128x128 | 1x | 128x128 |
| 128x128 | 2x | 256x256 |
| 256x256 | 1x | 256x256 |
| 256x256 | 2x | 512x512 |
| 512x512 | 1x | 512x512 |
| 512x512 | 2x | 1024x1024 |

---

## Contents.json Structure

The Asset Catalog uses `Contents.json` to define icon mappings.

### AppIcon.appiconset/Contents.json

```json
{
  "images": [
    {
      "size": "20x20",
      "idiom": "iphone",
      "filename": "Icon-20@2x.png",
      "scale": "2x"
    },
    {
      "size": "20x20",
      "idiom": "iphone",
      "filename": "Icon-20@3x.png",
      "scale": "3x"
    },
    {
      "size": "29x29",
      "idiom": "iphone",
      "filename": "Icon-29@2x.png",
      "scale": "2x"
    },
    {
      "size": "29x29",
      "idiom": "iphone",
      "filename": "Icon-29@3x.png",
      "scale": "3x"
    },
    {
      "size": "40x40",
      "idiom": "iphone",
      "filename": "Icon-40@2x.png",
      "scale": "2x"
    },
    {
      "size": "40x40",
      "idiom": "iphone",
      "filename": "Icon-40@3x.png",
      "scale": "3x"
    },
    {
      "size": "60x60",
      "idiom": "iphone",
      "filename": "Icon-60@2x.png",
      "scale": "2x"
    },
    {
      "size": "60x60",
      "idiom": "iphone",
      "filename": "Icon-60@3x.png",
      "scale": "3x"
    },
    {
      "size": "20x20",
      "idiom": "ipad",
      "filename": "Icon-20.png",
      "scale": "1x"
    },
    {
      "size": "20x20",
      "idiom": "ipad",
      "filename": "Icon-20@2x.png",
      "scale": "2x"
    },
    {
      "size": "29x29",
      "idiom": "ipad",
      "filename": "Icon-29.png",
      "scale": "1x"
    },
    {
      "size": "29x29",
      "idiom": "ipad",
      "filename": "Icon-29@2x.png",
      "scale": "2x"
    },
    {
      "size": "40x40",
      "idiom": "ipad",
      "filename": "Icon-40.png",
      "scale": "1x"
    },
    {
      "size": "40x40",
      "idiom": "ipad",
      "filename": "Icon-40@2x.png",
      "scale": "2x"
    },
    {
      "size": "76x76",
      "idiom": "ipad",
      "filename": "Icon-76.png",
      "scale": "1x"
    },
    {
      "size": "76x76",
      "idiom": "ipad",
      "filename": "Icon-76@2x.png",
      "scale": "2x"
    },
    {
      "size": "83.5x83.5",
      "idiom": "ipad",
      "filename": "Icon-83.5@2x.png",
      "scale": "2x"
    },
    {
      "size": "1024x1024",
      "idiom": "ios-marketing",
      "filename": "Icon-1024.png",
      "scale": "1x"
    }
  ],
  "info": {
    "version": 1,
    "author": "xcode"
  }
}
```

### Modern Single-Size Contents.json (iOS 18+/Xcode 15+)

```json
{
  "images": [
    {
      "filename": "AppIcon.png",
      "idiom": "universal",
      "platform": "ios",
      "size": "1024x1024"
    }
  ],
  "info": {
    "author": "xcode",
    "version": 1
  }
}
```

---

## Launch Screen / Splash Screen

iOS uses Launch Storyboards rather than static images. However, if you need launch images:

### Launch Image Sizes (Legacy)
| Device | Portrait | Landscape |
|--------|----------|-----------|
| iPhone SE | 640x1136 | 1136x640 |
| iPhone 8 | 750x1334 | 1334x750 |
| iPhone 8 Plus | 1242x2208 | 2208x1242 |
| iPhone X/XS/11 Pro | 1125x2436 | 2436x1125 |
| iPhone XR/11 | 828x1792 | 1792x828 |
| iPhone XS Max/11 Pro Max | 1242x2688 | 2688x1242 |
| iPhone 12 mini | 1080x2340 | 2340x1080 |
| iPhone 12/12 Pro | 1170x2532 | 2532x1170 |
| iPhone 12 Pro Max | 1284x2778 | 2778x1284 |
| iPhone 14 Pro | 1179x2556 | 2556x1179 |
| iPhone 14 Pro Max | 1290x2796 | 2796x1290 |
| iPhone 15/15 Pro | 1179x2556 | 2556x1179 |
| iPhone 15 Pro Max | 1290x2796 | 2796x1290 |
| iPad | 1536x2048 | 2048x1536 |
| iPad Pro 11" | 1668x2388 | 2388x1668 |
| iPad Pro 12.9" | 2048x2732 | 2732x2048 |

### Recommended Approach
Use a **Launch Storyboard** with:
- Auto Layout constraints
- Safe area compliance
- System background colors
- Vector assets or scalable images

---

## App Store Screenshot Requirements

### iPhone Screenshots
| Display Size | Portrait | Landscape |
|--------------|----------|-----------|
| 6.9" (15 Pro Max) | 1320x2868 | 2868x1320 |
| 6.7" (14 Pro Max) | 1290x2796 | 2796x1290 |
| 6.5" (11 Pro Max) | 1242x2688 | 2688x1242 |
| 5.5" (8 Plus) | 1242x2208 | 2208x1242 |

### iPad Screenshots
| Display Size | Portrait | Landscape |
|--------------|----------|-----------|
| 12.9" (Pro) | 2048x2732 | 2732x2048 |
| 11" (Pro) | 1668x2388 | 2388x1668 |

**Requirements:**
- PNG or JPEG format
- RGB color space
- No alpha channel for JPEG
- Minimum 3 screenshots, maximum 10 per device type

---

## Design Guidelines

### Icon Design Rules
1. **No transparency** - iOS icons cannot have transparent backgrounds
2. **No rounded corners in source** - iOS applies corner radius automatically
3. **Single, centered glyph** - Avoid complex scenes
4. **No text in icons** - Especially avoid app names
5. **Avoid photographs** - Use graphics and illustrations
6. **Consider Dark Mode** - Icons should work on both light/dark backgrounds

### Optical Sizing
- Circular icons should extend to edges
- Square icons need slight padding (~10%)
- Complex shapes need careful balance

### Color and Contrast
- High saturation works well at small sizes
- Avoid very thin lines (< 2pt at 1x)
- Test legibility at 29x29 actual size

---

## File Naming Conventions

```
AppIcon.appiconset/
├── Icon-20.png         (20x20)
├── Icon-20@2x.png      (40x40)
├── Icon-20@3x.png      (60x60)
├── Icon-29.png         (29x29)
├── Icon-29@2x.png      (58x58)
├── Icon-29@3x.png      (87x87)
├── Icon-40.png         (40x40)
├── Icon-40@2x.png      (80x80)
├── Icon-40@3x.png      (120x120)
├── Icon-60@2x.png      (120x120)
├── Icon-60@3x.png      (180x180)
├── Icon-76.png         (76x76)
├── Icon-76@2x.png      (152x152)
├── Icon-83.5@2x.png    (167x167)
├── Icon-1024.png       (1024x1024)
└── Contents.json
```

---

## Best Practices Summary

1. **Start with 1024x1024** - Scale down for all other sizes
2. **Use Asset Catalogs** - Never manually place icons in project folders
3. **Test at actual size** - View icons at their rendered sizes, not zoomed
4. **Provide all required sizes** - Missing sizes cause App Store rejection
5. **No alpha channel** - Especially for App Store submission
6. **Validate with Xcode** - Asset catalog warnings catch issues early
