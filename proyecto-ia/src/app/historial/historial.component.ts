import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

interface Analisis {
  id: number;
  fecha: string;
  diagnostico: string;
  explicacion: string;
  imagen: string;
}

@Component({
  selector: 'app-historial',
  imports: [RouterModule, CommonModule],
  templateUrl: './historial.component.html',
  styleUrl: './historial.component.scss'
})
export class HistorialComponent {
historial: Analisis[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.obtenerHistorial();
  }

  obtenerHistorial(): void {
    this.http.get<Analisis[]>('http://localhost:5000/historial').subscribe({
      next: (data) => {
        console.log('Datos recibidos:', data);
        this.historial = data;
      },
      error: (err) => console.error('Error al obtener historial', err)
    });
  }
}
