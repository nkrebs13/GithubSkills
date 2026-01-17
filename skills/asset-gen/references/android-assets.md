# Android Asset Requirements

## Launcher Icon (Mipmap) Sizes

Android uses density-independent pixels (dp) with different screen density buckets. Launcher icons should be placed in the `mipmap` directories.

| Density | Scale | Icon Size | Directory |
|---------|-------|-----------|-----------|
| mdpi | 1x | 48x48 px | `mipmap-mdpi/` |
| hdpi | 1.5x | 72x72 px | `mipmap-hdpi/` |
| xhdpi | 2x | 96x96 px | `mipmap-xhdpi/` |
| xxhdpi | 3x | 144x144 px | `mipmap-xxhdpi/` |
| xxxhdpi | 4x | 192x192 px | `mipmap-xxxhdpi/` |

### File Naming
- Legacy icon: `ic_launcher.png`
- Round icon: `ic_launcher_round.png`
- Foreground: `ic_launcher_foreground.png`
- Background: `ic_launcher_background.png`

---

## Adaptive Icons (Android 8.0+)

Adaptive icons provide a consistent appearance across different device manufacturers and launchers.

### Structure
```
res/
├── mipmap-anydpi-v26/
│   └── ic_launcher.xml
├── mipmap-xxxhdpi/
│   ├── ic_launcher_foreground.png
│   └── ic_launcher_background.png
```

### Foreground Layer
| Density | Canvas Size | Safe Zone |
|---------|-------------|-----------|
| mdpi | 108x108 px | 72x72 px center |
| hdpi | 162x162 px | 108x108 px center |
| xhdpi | 216x216 px | 144x144 px center |
| xxhdpi | 324x324 px | 216x216 px center |
| xxxhdpi | 432x432 px | 288x288 px center |

### Background Layer
Same dimensions as foreground. Can be:
- Solid color (defined in XML)
- Gradient (defined in XML)
- Image asset (PNG)

### Safe Zone Guidelines
- **Full canvas**: 108dp (432px at xxxhdpi)
- **Visible area**: Varies by launcher shape (66dp-72dp)
- **Safe zone for critical content**: 72dp centered (288px at xxxhdpi)
- Keep all important visual elements within the inner 66% of the canvas
- The outer 16dp on each side may be clipped by circular or squircle masks

### Adaptive Icon XML Template
```xml
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@mipmap/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
    <monochrome android:drawable="@mipmap/ic_launcher_monochrome"/>
</adaptive-icon>
```

### Monochrome Icon (Android 13+)
- Used for themed icons
- Single-color silhouette version
- Same 432x432 canvas at xxxhdpi
- Alpha channel only (white on transparent)

---

## Google Play Store Requirements

### App Icon
- **Size**: 512x512 pixels
- **Format**: PNG (32-bit with alpha)
- **Max file size**: 1024 KB
- **Shape**: Full bleed, square (Play Store applies rounding)
- **No badges or text overlays** recommending download/pricing

### Feature Graphic
- **Size**: 1024x500 pixels
- **Format**: PNG or JPEG (24-bit, no alpha)
- **Purpose**: Displayed in Play Store listings and promotions
- **Safe zone**: Keep critical content within center 920x400

### Screenshots
| Device Type | Minimum | Maximum per type |
|-------------|---------|------------------|
| Phone | 2 | 8 |
| 7-inch tablet | 0 | 8 |
| 10-inch tablet | 0 | 8 |
| Chromebook | 0 | 8 |
| Wear OS | 0 | 8 |
| Android TV | 0 | 8 |

**Screenshot requirements:**
- Minimum dimension: 320px
- Maximum dimension: 3840px
- Aspect ratio: 16:9 or 9:16
- Format: PNG or JPEG (no alpha)

### Promo Video
- YouTube URL
- Landscape orientation recommended
- No age-restricted content

### TV Banner (Android TV)
- **Size**: 1280x720 pixels
- **Format**: PNG or JPEG (24-bit)

---

## Notification Icons

### Requirements
- **Size at xxxhdpi**: 96x96 pixels (24dp base)
- Must be white silhouette on transparent background
- No color (system applies tint)
- Simple, recognizable shapes

| Density | Size |
|---------|------|
| mdpi | 24x24 px |
| hdpi | 36x36 px |
| xhdpi | 48x48 px |
| xxhdpi | 72x72 px |
| xxxhdpi | 96x96 px |

### Design Guidelines
- Use flat design (no gradients or shadows)
- Avoid fine details that won't render at small sizes
- Test visibility on both light and dark backgrounds
- Padding: 2dp on all sides for optical alignment

### File Location
```
res/
├── drawable-mdpi/
│   └── ic_notification.png
├── drawable-hdpi/
│   └── ic_notification.png
├── drawable-xhdpi/
│   └── ic_notification.png
├── drawable-xxhdpi/
│   └── ic_notification.png
└── drawable-xxxhdpi/
    └── ic_notification.png
```

---

## Action Bar / Toolbar Icons

| Density | Size |
|---------|------|
| mdpi | 24x24 px |
| hdpi | 36x36 px |
| xhdpi | 48x48 px |
| xxhdpi | 72x72 px |
| xxxhdpi | 96x96 px |

---

## Splash Screen (Android 12+)

### Adaptive Splash Icon
- Same structure as adaptive icons
- **Size**: 288x288 dp (1152x1152 px at xxxhdpi)
- **Branded image safe zone**: 200x200 dp centered (inner 2/3)
- Supports animated Vector Drawable (AVD)

### Window Background
- Solid color recommended
- Defined via `windowSplashScreenBackground` attribute

### Splash Screen Theme
```xml
<style name="Theme.App.Splash" parent="Theme.SplashScreen">
    <item name="windowSplashScreenBackground">@color/splash_bg</item>
    <item name="windowSplashScreenAnimatedIcon">@drawable/ic_splash</item>
    <item name="windowSplashScreenAnimationDuration">1000</item>
    <item name="postSplashScreenTheme">@style/Theme.App</item>
</style>
```

---

## Best Practices Summary

1. **Always provide all density variants** - Android will scale if missing, but quality suffers
2. **Design at xxxhdpi first** - Scale down for lower densities
3. **Test on multiple launchers** - Icon shapes vary (circle, squircle, rounded square)
4. **Use vector assets where possible** - For everything except launcher icons
5. **Keep adaptive icon layers aligned** - Background and foreground should share visual center
6. **Verify safe zone compliance** - Critical content must survive circular cropping
