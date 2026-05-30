import { ChangeDetectorRef, Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VoiceChatComponent } from "../voice-chat/voice-chat.component";
import { VoiceService } from '../../services/voice.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, VoiceChatComponent],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent {

  repoUrl = '';
  repoName = '';
  question = '';
  dbQuestion = '';

  answer: any = null;
  dbResponse: any = null;
  isRecording: boolean = false;
  mediaRecorder!: MediaRecorder;
  audioChunks: Blob[] = [];
  mode: string = '';

  constructor(private api: ApiService,  private cdr: ChangeDetectorRef,private voiceService: VoiceService) {}

  cloneRepository() {

    this.api.cloneRepository(this.repoUrl)
      .subscribe((res: any) => {

        this.repoName = res.repo_name;

        alert('Repository indexed successfully');
      });
  }

  askCodebase() {

    this.api.chatCodebase(
      this.repoName,
      this.question
    ).subscribe((res: any) => {

      this.answer = res.answer;
      this.cdr.detectChanges();
    });
  }

  askDatabase() {

    this.api.askDatabase(
      this.dbQuestion
    ).subscribe((res: any) => {

      this.dbResponse = res;
      this.cdr.detectChanges();
    });
  }

  async startRecording() {

    try {

      this.isRecording = true;
      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: true
        });

      this.mediaRecorder =
        new MediaRecorder(stream);

      this.audioChunks = [];

      this.mediaRecorder.ondataavailable =
        (event: BlobEvent) => {

          if (event.data.size > 0) {
            this.audioChunks.push(event.data);
          }

        };

      this.mediaRecorder.onstop = () => {

        const audioBlob = new Blob(
          this.audioChunks,
          { type: 'audio/wav' }
        );

        // API CALL ON STOP
        this.sendAudio(audioBlob);

      };

      this.mediaRecorder.start();


    } catch (error) {

      console.error(error);

      alert('Microphone permission denied');

    }
  }

  stopRecording(strMode: string) {

    if (this.mediaRecorder) {
      this.mode = strMode;
      this.mediaRecorder.stop();

      this.isRecording = false;

    }

  }

  sendAudio(audioBlob: Blob) {

    this.voiceService
      .sendVoice(audioBlob, this.mode, this.mode === "repo" ? this.repoName : "")
      .subscribe({

        next: (res: any) => {

          console.log(res);

          this.answer = res.answer;

          // Play AI Voice Response
          const audio = new Audio(
            `http://localhost:8000${res.audio_url}`
          );

          audio.play();

        },

        error: (err) => {

          console.error(err);

        }

      });

  }
}