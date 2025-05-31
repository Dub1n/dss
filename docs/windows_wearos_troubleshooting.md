---
tags: [troubleshooting, windows, wearos, development]
provides: [windows_wearos_troubleshooting]
requires: [meta/templates/wearos_project_structure.md]
---

# Windows WearOS Development Troubleshooting

This guide addresses common issues encountered by Windows users developing WearOS applications, based on DSS installation report analysis.

## Common Installation Issues

### 1. Console Encoding Problems

**Symptoms:**
- Unicode characters display as `?` or boxes
- Console output appears garbled
- Build logs are unreadable

**Solutions:**
```powershell
# Set console encoding (PowerShell)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Set environment variables
$env:PYTHONIOENCODING = "utf-8"
$env:JAVA_OPTS = "-Dfile.encoding=UTF-8"
```

**For Android Studio:**
1. Go to `Help` → `Edit Custom VM Options`
2. Add: `-Dfile.encoding=UTF-8`
3. Restart Android Studio

### 2. Path Length Limitations

**Symptoms:**
- "Path too long" errors during build
- Gradle sync failures
- File system errors

**Solutions:**
```powershell
# Enable long path support (requires admin)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

**Alternative approaches:**
- Use shorter project directory names
- Move project closer to root (e.g., `C:\dev\myproject`)
- Use junction points for deep nested structures

### 3. WearOS Emulator Issues

**Symptoms:**
- Emulator fails to start
- Poor performance
- Connection timeouts

**Solutions:**

#### Enable Hyper-V (Windows 10 Pro/Enterprise)
```powershell
# Run as administrator
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

#### Configure Emulator Settings
```bash
# In Android Studio AVD Manager
# For WearOS emulator, use these settings:
# - RAM: 1GB minimum
# - Heap: 256MB
# - Graphics: Hardware - GLES 2.0
```

#### Alternative: Use Physical Device
```bash
# Enable ADB over WiFi for WearOS watch
adb tcpip 5555
adb connect [WATCH_IP]:5555
```

## Build System Issues

### 1. Gradle Build Failures

**Common error:** `Could not resolve all files for configuration`

**Solution:**
```gradle
// In module build.gradle
android {
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = '11'
    }
}
```

### 2. WearOS Dependencies

**Error:** `Cannot resolve androidx.wear:wear`

**Solution:**
```gradle
// Ensure correct repositories
repositories {
    google()
    mavenCentral()
}

dependencies {
    implementation 'androidx.wear:wear:1.3.0'
    compileOnly 'com.google.android.wearable:wearable:2.9.0'
    
    // For data layer communication
    implementation 'com.google.android.gms:play-services-wearable:18.0.0'
}
```

### 3. Manifest Configuration Issues

**Error:** `INSTALL_FAILED_MISSING_FEATURE`

**Solution:**
```xml
<!-- In wear module AndroidManifest.xml -->
<uses-feature android:name="android.hardware.type.watch" />

<!-- For standalone apps -->
<meta-data android:name="com.google.android.wearable.standalone"
           android:value="true" />

<!-- For companion apps -->
<meta-data android:name="com.google.android.wearable.standalone"
           android:value="false" />
```

## Development Environment Setup

### 1. Android Studio Configuration

**Recommended settings for Windows WearOS development:**

```properties
# In gradle.properties
org.gradle.jvmargs=-Xmx4096m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.configureondemand=true
android.useAndroidX=true
android.enableJetifier=true
```

### 2. SDK Manager Setup

**Required components:**
- Android SDK Platform 33 (minimum)
- Android SDK Build-Tools 33.0.0+
- Google Play services
- Google Repository
- Wear OS by Google System Images

### 3. Device Connection

**For WearOS watch over USB:**
```bash
# Enable developer options on watch
# Settings → System → About → Build number (tap 7 times)

# Enable ADB debugging
# Settings → Developer options → ADB debugging

# Verify connection
adb devices
# Should show: [DEVICE_ID] device
```

## Performance Optimization

### 1. Build Performance

**Optimize Gradle builds:**
```gradle
// In module build.gradle
android {
    buildTypes {
        debug {
            minifyEnabled false
            // Disable PNG crunching for faster builds
            crunchPngs false
        }
    }
    
    // Use dex-in-process for faster builds
    dexOptions {
        dexInProcess true
        preDexLibraries true
        maxProcessCount 8
    }
}
```

### 2. Emulator Performance

**Windows-specific optimizations:**
1. **Disable Windows Defender real-time scanning** for Android SDK directory
2. **Exclude from virus scanning:**
   - `%USERPROFILE%\.android\`
   - Android Studio installation directory
   - Project directories

3. **Increase virtual memory:**
   - Control Panel → System → Advanced → Performance Settings
   - Set virtual memory to 1.5x physical RAM

## Debugging WearOS Applications

### 1. Logcat Filtering

**View WearOS-specific logs:**
```bash
# Filter by package name
adb logcat | grep "com.yourpackage"

# Filter by tag
adb logcat -s "WearableListenerService"

# View all wear-related logs
adb logcat | grep -i wear
```

### 2. Data Layer Debugging

**Common debugging commands:**
```bash
# Check data layer connection
adb shell dumpsys activity service com.google.android.gms.wearable

# View MessageClient messages
adb logcat -s "MessageClient"

# View DataClient synchronization
adb logcat -s "DataClient"
```

## DSS Integration Fixes

### 1. Bootstrap Console Issues

If you encounter console issues during DSS bootstrap:

```powershell
# Run bootstrap with explicit encoding
$env:PYTHONIOENCODING = "utf-8"
python dss_bootstrap.py
```

### 2. File Organization

For WearOS projects, use the template structure:
```
# After DSS transformation, reorganize as:
src/
├── wear/     # WearOS module
├── mobile/   # Companion app
└── shared/   # Common code
```

### 3. Template Integration

**Apply WearOS template after DSS transformation:**
1. Copy `meta/templates/wearos_project_structure.md` guidance
2. Reorganize modules according to template
3. Update `docs/` with WearOS-specific documentation
4. Configure `meta/wearos-config.yml`

## Frequently Asked Questions

### Q: Emulator is extremely slow on Windows
**A:** 
1. Enable Hyper-V if using Windows Pro/Enterprise
2. Increase allocated RAM in AVD Manager
3. Use x86_64 system images instead of ARM
4. Consider using a physical device for development

### Q: Build fails with "Could not find androidx.wear"
**A:**
1. Ensure Google repository is enabled in build.gradle
2. Sync project with Gradle files
3. Clean and rebuild project
4. Update to latest WearOS dependencies

### Q: ADB doesn't detect my WearOS device
**A:**
1. Enable Developer Options on watch
2. Enable ADB debugging in Developer Options
3. Install Google USB drivers
4. Try different USB ports/cables
5. Use `adb kill-server && adb start-server`

### Q: WearOS app installs but doesn't appear on watch
**A:**
1. Check if companion app is required and installed
2. Verify manifest has correct `uses-feature` declarations
3. Ensure watch and phone are paired properly
4. Check if app appears in watch's app drawer (not just on face)

## Getting Help

If you continue experiencing issues:

1. **Check DSS installation reports** for similar patterns
2. **Submit installation report** to DSS repository with Windows/WearOS labels
3. **Consult WearOS documentation**: [developer.android.com/wear](https://developer.android.com/wear)
4. **Android Studio issues**: [developer.android.com/studio/troubleshoot](https://developer.android.com/studio/troubleshoot)

---

*This guide is based on analysis of installation reports from Windows WearOS developers using DSS.* 