import { Component, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-image',
  standalone: true,
  imports: [CommonModule,RouterModule],
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.scss']
})
export class ImageComponent {
  selectedImage: File | null = null;
  imagePreview: string | ArrayBuffer | null = null;
  predictionResult: string = '';
  loading = false;
  cameraActive = false;
  @ViewChild('audioPlayer') audioPlayer!: ElementRef<HTMLAudioElement>;
  audioUrl: string | null = null;

  @ViewChild('video') videoElement!: ElementRef;
  @ViewChild('canvas') canvasElement!: ElementRef;
  videoStream: MediaStream | null = null;

  constructor(private http: HttpClient) { }

  onFileSelected(event: any): void {
    this.selectedImage = event.target.files[0];
    const reader = new FileReader();
    reader.onload = () => this.imagePreview = reader.result;
    reader.readAsDataURL(this.selectedImage!);
  }

  startCamera(): void {
    this.cameraActive = true;
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        this.videoStream = stream;
        this.videoElement.nativeElement.srcObject = stream;
      })
      .catch(err => {
        console.error('No se pudo acceder a la cámara:', err);
        this.cameraActive = false;
      });
  }

  stopCamera(): void {
    if (this.videoStream) {
      this.videoStream.getTracks().forEach(track => track.stop());
    }
    this.cameraActive = false;
  }

  capturePhoto(): void {
    const video = this.videoElement.nativeElement;
    const canvas = this.canvasElement.nativeElement;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob: Blob | null) => {
      if (blob) {
        this.selectedImage = new File([blob], 'captura.jpg', { type: 'image/jpeg' });

        const reader = new FileReader();
        reader.onload = () => this.imagePreview = reader.result;
        reader.readAsDataURL(this.selectedImage!);
        this.stopCamera();
      }
    }, 'image/jpeg');

  }

  uploadImage(): void {
  if (!this.selectedImage) return;

  const formData = new FormData();
  formData.append('image', this.selectedImage);
  this.loading = true;
  this.predictionResult = '';
  this.audioUrl = null;

  this.http.post('http://localhost:5000/predict', formData, {
    responseType: 'blob'  // 👈 importante para recibir audio
  }).subscribe({
    next: blob => {
      this.audioUrl = URL.createObjectURL(blob);

      const audio = this.audioPlayer.nativeElement;
      audio.load(); // fuerza a actualizar el reproductor
      audio.play(); // lo reproduce automáticamente

      // También podrías decodificar texto si el backend lo enviara como JSON.
      this.predictionResult = 'Análisis completado. Escuche el resultado.';
      this.loading = false;
    },
    error: err => {
      this.predictionResult = 'Error al procesar la imagen.';
      this.loading = false;
    }
  });
}

}
