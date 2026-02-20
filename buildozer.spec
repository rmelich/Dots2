[app]
title = Dots2
package.name = dots2
package.domain = org.example
version = 0.1.0

source.dir = .
source.include_exts = py,wav,png,jpg,jpeg,ttf,txt,json,ogg
requirements = python3==3.10.13,pygame,cython==0.29.36

android.archs = arm64-v8a,armeabi-v7a
android.api = 33
android.minapi = 21

android.sdk_path = /home/runner/android-sdk
android.sdkmanager_path = /home/runner/android-sdk/cmdline-tools/latest/bin/sdkmanager
android.ndk_path = /home/runner/android-ndk
android.ndk = 25b

log_level = 2


