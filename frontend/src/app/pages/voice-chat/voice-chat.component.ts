import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  inject,
  signal
} from '@angular/core';
import { VoiceService } from '../../services/voice.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-voice-chat',
  templateUrl: './voice-chat.component.html',
  standalone: true,
  imports: [FormsModule,CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class VoiceChatComponent {

  // mediaRecorder!: MediaRecorder;

  // audioChunks: Blob[] = [];

  // isRecording = false;

  // answer = '';
  // mode: string = '';
  // constructor(
  //   private voiceService: VoiceService
  // ) {}

  // async startRecording() {

  //   try {

  //     const stream =
  //       await navigator.mediaDevices.getUserMedia({
  //         audio: true
  //       });

  //     this.mediaRecorder =
  //       new MediaRecorder(stream);

  //     this.audioChunks = [];

  //     this.mediaRecorder.ondataavailable =
  //       (event: BlobEvent) => {

  //         if (event.data.size > 0) {
  //           this.audioChunks.push(event.data);
  //         }

  //       };

  //     this.mediaRecorder.onstop = () => {

  //       const audioBlob = new Blob(
  //         this.audioChunks,
  //         { type: 'audio/wav' }
  //       );

  //       // API CALL ON STOP
  //       this.sendAudio(audioBlob);

  //     };

  //     this.mediaRecorder.start();

  //     this.isRecording = true;

  //   } catch (error) {

  //     console.error(error);

  //     alert('Microphone permission denied');

  //   }
  // }

  // stopRecording(strMode: string) {

  //   if (this.mediaRecorder) {
  //     this.mode = strMode;
  //     this.mediaRecorder.stop();

  //     this.isRecording = false;

  //   }

  // }

  // sendAudio(audioBlob: Blob) {

  //   this.voiceService
  //     .sendVoice(audioBlob, this.mode)
  //     .subscribe({

  //       next: (res: any) => {

  //         console.log(res);

  //         this.answer = res.answer;

  //         // Play AI Voice Response
  //         const audio = new Audio(
  //           `http://localhost:8000${res.audio_url}`
  //         );

  //         audio.play();

  //       },

  //       error: (err) => {

  //         console.error(err);

  //       }

  //     });

  // }

  private readonly destroyRef = inject(DestroyRef);

  private mediaRecorder?: MediaRecorder;

  private audioChunks: Blob[] = [];

  readonly isRecording = signal(false);

  readonly isLoading = signal(false);

  readonly transcript = signal('');

  readonly aiResponse = signal('');

  readonly waveformBars =
    Array.from({ length: 42 });

  constructor(private voiceService: VoiceService) {

    this.destroyRef.onDestroy(() => {
      this.stopTracks();
    });

  }

  async toggleRecording(): Promise<void> {

    if (this.isRecording()) {
      this.stopRecording();
      return;
    }

    await this.startRecording();

  }

  private async startRecording(): Promise<void> {

    try {

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

      this.mediaRecorder.onstop = async () => {

        const audioBlob = new Blob(
          this.audioChunks,
          {
            type: 'audio/wav'
          }
        );

        await this.uploadAudio(audioBlob);

      };

      this.mediaRecorder.start();

      this.isRecording.set(true);

    } catch (error) {

      console.error(error);

      alert('Microphone access denied');

    }

  }

  private stopRecording(): void {

    if (!this.mediaRecorder) {
      return;
    }

    this.mediaRecorder.stop();

    this.stopTracks();

    this.isRecording.set(false);

  }

  private stopTracks(): void {

    const tracks =
      this.mediaRecorder?.stream?.getTracks() || [];

    tracks.forEach(track => track.stop());

  }

  private async uploadAudio(
    audioBlob: Blob
  ): Promise<void> {

    try {

      this.isLoading.set(true);

      this.transcript.set('');

      this.aiResponse.set('');

      // const formData = new FormData();

      // formData.append(
      //   'file',
      //   audioBlob,
      //   'voice.wav'
      // );

      // const response: any =
      //   await this.http.post(
      //     'http://localhost:8000/api/voice-chat',
      //     formData
      //   ).toPromise();

      // const response: any = this.voiceService.sendVoice(audioBlob).toPromise();
      this.voiceService.sendVoice(audioBlob).subscribe({
        next: async (response: any) => {
          this.transcript.set(
            response?.transcript || ''
          );

          this.aiResponse.set(
            response?.response || ''
          );

          // Auto Play AI Audio
          if (response?.audio_url) {

            const audio =
              new Audio(
                `http://localhost:8000/${response.audio_url}`
              );

            await audio.play();

          }
        }
      })
      

    } catch (error) {

      console.error(error);

      alert('Voice API Error');

    } finally {

      this.isLoading.set(false);

    }

  }
}