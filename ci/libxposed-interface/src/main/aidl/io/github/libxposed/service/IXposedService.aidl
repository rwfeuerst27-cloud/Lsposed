package io.github.libxposed.service;

import io.github.libxposed.service.IXposedScopeCallback;
import android.os.Bundle;
import android.os.ParcelFileDescriptor;

interface IXposedService {
    const int API = 100;
    const int FRAMEWORK_PRIVILEGE_ROOT = 0;
    const int FRAMEWORK_PRIVILEGE_CONTAINER = 1;
    const int FRAMEWORK_PRIVILEGE_APP = 2;

    int getAPIVersion();
    String getFrameworkName();
    String getFrameworkVersion();
    long getFrameworkVersionCode();
    int getFrameworkPrivilege();
    List<String> getScope();
    void requestScope(String packageName, IXposedScopeCallback callback);
    String removeScope(String packageName);
    Bundle requestRemotePreferences(String group);
    void updateRemotePreferences(String group, in Bundle diff);
    void deleteRemotePreferences(String group);
    String[] listRemoteFiles();
    ParcelFileDescriptor openRemoteFile(String path);
    boolean deleteRemoteFile(String path);
}
