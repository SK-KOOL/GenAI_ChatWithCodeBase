import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class VoiceService {

  apiUrl = 'http://localhost:8000/api/voice-chat';

  constructor(private http: HttpClient) {}

  sendVoice(blob: Blob, mode: string = 'repo', repo_name: string = '') {

    // Convert Blob to File
    const audioFile = new File(
      [blob],
      'recording.wav',
      { type: 'audio/wav' }
    );

    const formData = new FormData();

    // IMPORTANT
    formData.append('file', audioFile);

    return this.http.post(
      `${this.apiUrl}?mode=${mode}&repo_name=${repo_name}`,
      formData
    );
  }
}