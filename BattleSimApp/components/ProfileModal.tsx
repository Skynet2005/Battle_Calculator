import React from "react";
import { Modal, View, Text, TouchableOpacity, StyleSheet, Platform, useWindowDimensions } from "react-native";
import { ProfileSection } from "./ProfileSection";
import { SavedSettingsData, AuthState } from "../types";
import { styles } from "../styles";

interface ProfileModalProps {
  visible: boolean;
  onClose: () => void;
  collectSettings: () => SavedSettingsData;
  applySettings: (data: SavedSettingsData) => void;
  onAuthChange?: (auth: AuthState | null) => void;
}

export const ProfileModal: React.FC<ProfileModalProps> = ({
  visible,
  onClose,
  collectSettings,
  applySettings,
  onAuthChange,
}) => {
  const { width, height } = useWindowDimensions();
  const isMobile = width < 768;
  const isTablet = width >= 768 && width < 1024;

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={true}
      onRequestClose={onClose}
    >
      <View style={modalStyles.overlay}>
        <View style={[
          modalStyles.modal,
          isMobile ? modalStyles.modalMobile : 
          isTablet ? modalStyles.modalTablet : 
          modalStyles.modalDesktop
        ]}>
          <View style={modalStyles.header}>
            <Text style={modalStyles.title}>Profile & Settings</Text>
            <TouchableOpacity style={modalStyles.closeButton} onPress={onClose}>
              <Text style={modalStyles.closeText}>✕</Text>
            </TouchableOpacity>
          </View>
          
          <View style={modalStyles.content}>
            <ProfileSection
              collectSettings={collectSettings}
              applySettings={applySettings}
              onAuthChange={onAuthChange}
              minimal={false}
            />
          </View>
        </View>
      </View>
    </Modal>
  );
};

const modalStyles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    justifyContent: "center",
    alignItems: "center",
    padding: 16,
  },
  modal: {
    backgroundColor: "#1F2937",
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#374151",
    maxHeight: "90%",
    ...(Platform.OS === "web" ? {
      boxShadow: "0 10px 25px rgba(0,0,0,0.3)"
    } : {
      shadowColor: "#000",
      shadowOffset: { width: 0, height: 10 },
      shadowOpacity: 0.3,
      shadowRadius: 25,
      elevation: 10,
    }),
  },
  modalMobile: {
    width: "100%",
    maxWidth: 400,
  },
  modalTablet: {
    width: "100%",
    maxWidth: 768,
  },
  modalDesktop: {
    width: "100%",
    maxWidth: 1024,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: "#374151",
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#F1F5F9",
  },
  closeButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: "#374151",
    justifyContent: "center",
    alignItems: "center",
  },
  closeText: {
    color: "#E5E7EB",
    fontSize: 16,
    fontWeight: "bold",
  },
  content: {
    padding: 20,
  },
});
