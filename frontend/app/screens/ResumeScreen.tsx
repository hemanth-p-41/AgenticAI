import React, { useState } from 'react';
import { View, Text, Button, Platform } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import { uploadResume, getResume } from '../services/resumeService';
import { useAuth } from '../hooks/useAuth';

export default function ResumeScreen() {
  const { token } = useAuth();
  const [info, setInfo] = useState<any>(null);

  const pickAndUpload = async () => {
    const res = await DocumentPicker.getDocumentAsync({ type: 'application/pdf' });
    if (res.type === 'success') {
      // create file object for FormData
      const file: any = {
        uri: res.uri,
        name: res.name,
        type: 'application/pdf',
      };
      const up = await uploadResume(file, token as string);
      const full = await getResume(up.id, token as string);
      setInfo(full);
    }
  };

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 20 }}>Resume</Text>
      <Button title="Upload PDF" onPress={pickAndUpload} />
      {info ? (
        <View style={{ marginTop: 12 }}>
          <Text>Skills: {(info.analysis?.skills || []).join(', ')}</Text>
          <Text>Projects: {(info.analysis?.projects || []).join(', ')}</Text>
          <Text>Technologies: {(info.analysis?.technologies || []).join(', ')}</Text>
        </View>
      ) : null}
    </View>
  );
}
