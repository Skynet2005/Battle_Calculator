import React, { useCallback, useEffect, useMemo, useState } from "react";
import { View, Text, TextInput, TouchableOpacity, Alert, Platform } from "react-native";
import * as SecureStore from "expo-secure-store";
import axios from "axios";
import { AuthState, SavedSettingsData } from "../types";
import { styles } from "../styles";

interface Props {
  collectSettings: () => SavedSettingsData;
  applySettings: (data: SavedSettingsData) => void;
  onAuthChange?: (auth: AuthState | null) => void;
  minimal?: boolean;
}

export const ProfileSection: React.FC<Props> = ({ collectSettings, applySettings, onAuthChange, minimal }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [auth, setAuth] = useState<AuthState>({ token: null, username: null });
  const [busy, setBusy] = useState(false);
  const [presets, setPresets] = useState<Array<{ id: number; name: string; updated_at: string }>>([]);
  const [presetName, setPresetName] = useState("");

  const isLoggedIn = !!auth.token;

  // simple cross-platform storage shim (SecureStore on native, localStorage on web)
  const storage = {
    getItem: async (k: string): Promise<string | null> => {
      if (Platform.OS === "web") {
        try { return window.localStorage.getItem(k); } catch { return null; }
      }
      return SecureStore.getItemAsync(k);
    },
    setItem: async (k: string, v: string): Promise<void> => {
      if (Platform.OS === "web") {
        try { window.localStorage.setItem(k, v); } catch {}
        return;
      }
      await SecureStore.setItemAsync(k, v);
    },
    deleteItem: async (k: string): Promise<void> => {
      if (Platform.OS === "web") {
        try { window.localStorage.removeItem(k); } catch {}
        return;
      }
      await SecureStore.deleteItemAsync(k);
    },
  };

  useEffect(() => {
    // Created Logic for review: load token at mount
    (async () => {
      const token = await storage.getItem("auth_token");
      const uname = await storage.getItem("auth_username");
      if (token && uname) {
        const next = { token, username: uname } as AuthState;
        setAuth(next);
        onAuthChange?.(next);
      } else {
        onAuthChange?.(null);
      }
    })();
  }, []);

  const saveAuth = async (token: string, uname: string) => {
    await storage.setItem("auth_token", token);
    await storage.setItem("auth_username", uname);
    const next = { token, username: uname } as AuthState;
    setAuth(next);
    onAuthChange?.(next);
  };

  const clearAuth = async () => {
    await storage.deleteItem("auth_token");
    await storage.deleteItem("auth_username");
    setAuth({ token: null, username: null });
    onAuthChange?.(null);
  };

  const api = useMemo(() => {
    const inst = axios.create({ baseURL: "http://localhost:8000" });
    inst.interceptors.request.use((cfg) => {
      if (auth.token) cfg.headers = { ...(cfg.headers || {}), Authorization: `Bearer ${auth.token}` } as any;
      return cfg;
    });
    return inst;
  }, [auth.token]);

  const refreshPresets = useCallback(async () => {
    if (!isLoggedIn) { setPresets([]); return; }
    try {
      const r = await api.get("/api/settings/saved");
      const items = (r.data?.items || []) as Array<{ id: number; name: string; updated_at: string }>;
      setPresets(items);
    } catch {}
  }, [api, isLoggedIn]);

  const doRegister = async () => {
    if (!username || !password) return Alert.alert("Register", "Enter username and password");
    setBusy(true);
    try {
      const r = await api.post("/api/auth/register", { username, password });
      const { token, username: uname } = r.data as { token: string; username: string };
      await saveAuth(token, uname);
      Alert.alert("Register", "Account created and logged in");
      await refreshPresets();
    } catch (e: any) {
      Alert.alert("Register Failed", String(e.response?.data ?? e.message));
    } finally {
      setBusy(false);
    }
  };

  const doLogin = async () => {
    if (!username || !password) return Alert.alert("Login", "Enter username and password");
    setBusy(true);
    try {
      const r = await api.post("/api/auth/login", { username, password });
      const { token, username: uname } = r.data as { token: string; username: string };
      await saveAuth(token, uname);
      Alert.alert("Login", "Logged in");
      await refreshPresets();
    } catch (e: any) {
      Alert.alert("Login Failed", String(e.response?.data ?? e.message));
    } finally {
      setBusy(false);
    }
  };

  const doSaveSettings = async () => {
    if (!isLoggedIn) return Alert.alert("Save Settings", "Please log in first");
    setBusy(true);
    try {
      const data = collectSettings();
      await api.post("/api/settings", { data });
      Alert.alert("Settings", "Saved");
    } catch (e: any) {
      Alert.alert("Save Failed", String(e.response?.data ?? e.message));
    } finally {
      setBusy(false);
    }
  };

  const doLoadSettings = async () => {
    if (!isLoggedIn) return Alert.alert("Load Settings", "Please log in first");
    setBusy(true);
    try {
      const r = await api.get("/api/settings");
      const data = (r.data?.data || {}) as SavedSettingsData;
      applySettings(data);
      Alert.alert("Settings", "Loaded and applied");
    } catch (e: any) {
      Alert.alert("Load Failed", String(e.response?.data ?? e.message));
    } finally {
      setBusy(false);
    }
  };

  // Named presets
  const doSaveAsPreset = async () => {
    if (!isLoggedIn) return Alert.alert("Save Preset", "Please log in first");
    const name = (presetName || "Untitled").trim();
    if (!name) return Alert.alert("Save Preset", "Enter a name");
    setBusy(true);
    try {
      const data = collectSettings();
      const r = await api.post("/api/settings/saved", { name, data });
      setPresetName("");
      await refreshPresets();
      Alert.alert("Preset", `Saved as "${r.data?.name || name}"`);
    } catch (e: any) {
      Alert.alert("Save Preset Failed", String(e.response?.data ?? e.message));
    } finally {
      setBusy(false);
    }
  };

  const doLoadPreset = async (id: number) => {
    if (!isLoggedIn) return;
    setBusy(true);
    try {
      const r = await api.get(`/api/settings/saved/${id}`);
      const data = (r.data?.data || {}) as SavedSettingsData;
      applySettings(data);
      Alert.alert("Preset", "Loaded");
    } catch (e: any) {
      Alert.alert("Load Preset Failed", String(e.response?.data ?? e.message));
    } finally {
      setBusy(false);
    }
  };

  const doDeletePreset = async (id: number) => {
    if (!isLoggedIn) return;
    setBusy(true);
    try {
      await api.delete(`/api/settings/saved/${id}`);
      await refreshPresets();
    } catch (e: any) {
      Alert.alert("Delete Preset Failed", String(e.response?.data ?? e.message));
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => { refreshPresets(); }, [refreshPresets]);

  return (
    <View style={[styles.panel, { marginBottom: 12 }]}> 
      <Text style={styles.subHeader}>Profile</Text>
      {isLoggedIn ? (
        <Text style={styles.helperText}>Logged in as {auth.username}</Text>
      ) : (
        <Text style={styles.helperText}>Not logged in</Text>
      )}
      {!isLoggedIn && (
        <>
          <Text style={styles.label}>Username</Text>
          <TextInput value={username} onChangeText={setUsername} style={styles.input} autoCapitalize="none" editable={!busy} />
          <Text style={styles.label}>Password</Text>
          <TextInput value={password} onChangeText={setPassword} style={styles.input} secureTextEntry editable={!busy} />
          <View style={styles.actionsRow}>
            <View style={{ flex: 1 }}>
              <TouchableOpacity onPress={doLogin} disabled={busy} style={styles.buttonContainer}>
                <Text style={styles.buttonText}>Login</Text>
              </TouchableOpacity>
            </View>
            <View style={{ flex: 1 }}>
              <TouchableOpacity onPress={doRegister} disabled={busy} style={styles.secondaryButtonContainer}>
                <Text style={styles.buttonText}>Register</Text>
              </TouchableOpacity>
            </View>
          </View>
        </>
      )}
      {isLoggedIn && !minimal && (
        <View style={styles.actionsRow}>
          <View style={{ flex: 1 }}>
            <TouchableOpacity onPress={doSaveSettings} disabled={busy} style={styles.buttonContainer}>
              <Text style={styles.buttonText}>Save Settings</Text>
            </TouchableOpacity>
          </View>
          <View style={{ flex: 1 }}>
            <TouchableOpacity onPress={doLoadSettings} disabled={busy} style={styles.secondaryButtonContainer}>
              <Text style={styles.buttonText}>Load Settings</Text>
            </TouchableOpacity>
          </View>
          <View style={{ flex: 1 }}>
            <TouchableOpacity onPress={clearAuth} disabled={busy} style={styles.dangerButtonContainer}>
              <Text style={styles.buttonText}>Logout</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}

      {isLoggedIn && !minimal && (
        <View style={[styles.panel, { marginTop: 8 }]}> 
          <Text style={styles.subHeader}>Presets</Text>
          <Text style={styles.label}>Preset Name</Text>
          <TextInput value={presetName} onChangeText={setPresetName} style={styles.input} editable={!busy} placeholder="e.g., Rally vs. Marksmen" />
          <View style={styles.actionsRow}>
            <View style={{ flex: 1 }}>
              <TouchableOpacity onPress={doSaveAsPreset} disabled={busy} style={styles.buttonContainer}>
                <Text style={styles.buttonText}>Save As Preset</Text>
              </TouchableOpacity>
            </View>
            <View style={{ flex: 1 }}>
              <TouchableOpacity onPress={refreshPresets} disabled={busy} style={styles.secondaryButtonContainer}>
                <Text style={styles.buttonText}>Refresh List</Text>
              </TouchableOpacity>
            </View>
          </View>

          {presets.length === 0 ? (
            <Text style={styles.helperText}>No presets yet.</Text>
          ) : (
            <View style={styles.tableContainer}>
              <View style={styles.tableHeaderRow}>
                <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Name</Text>
                <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Updated</Text>
                <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Actions</Text>
              </View>
              {presets.map((p) => (
                <View key={`preset-${p.id}`} style={styles.tableRow}>
                  <Text style={[styles.tableCell, { flex: 2 }]}>{p.name}</Text>
                  <Text style={[styles.tableCell, { flex: 2 }]}>{new Date(p.updated_at).toLocaleString()}</Text>
                  <View style={{ flex: 1, flexDirection: 'row', justifyContent: 'flex-end' }}>
                    <TouchableOpacity style={styles.miniButton} onPress={() => doLoadPreset(p.id)}>
                      <Text style={styles.miniButtonText}>Load</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={styles.miniButton} onPress={() => doDeletePreset(p.id)}>
                      <Text style={styles.miniButtonText}>Delete</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              ))}
            </View>
          )}
        </View>
      )}
    </View>
  );
};


