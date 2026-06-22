package io.github.libxposed.service;

oneway interface IXposedScopeCallback {
    void onScopeRequestApproved(String packageName);
    void onScopeRequestDenied(String packageName);
    void onScopeRequestFailed(String packageName, String reason);
    void onScopeRequestTimeout(String packageName);
}
