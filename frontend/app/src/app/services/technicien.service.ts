// src/app/services/technicien.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export interface Technicien {
  id?: number;
  nom: string;
  email: string;
  type?: string;
  equipe?: string;
  poste?: string;
  telephone?: string;
  adresse?: string;
  is_active?: boolean;
  tache_id?: number;
  avatar_url?: string;

  // 🔥 Nécessaire car tu l’utilises dans techniciens.component.ts
  note_id?: number | null;
}

@Injectable({
  providedIn: 'root'
})
export class TechnicienService {

  //private baseUrl = 'http://127.0.0.1:8000/';
  private baseUrl = 'https://mongestionnaireapp.onrender.com/';


  constructor(private http: HttpClient) {}

  getTechniciens(): Observable<Technicien[]> {
    return this.http
      .get<{ status: string; data: Technicien[] }>(`${this.baseUrl}techniciens/`)
      .pipe(map(res => res.data));
  }

  getTechnicienById(id: number): Observable<Technicien> {
    return this.http
      .get<{ status: string; data: Technicien }>(`${this.baseUrl}techniciens/${id}`)
      .pipe(map(res => res.data));
  }

  // 🔥 UPDATE
  updateTechnicien(id: number, data: Partial<Technicien>): Observable<Technicien> {
    return this.http
      .put<{ status: string; data: Technicien }>(`${this.baseUrl}techniciens/${id}`, data)
      .pipe(map(res => res.data));
  }

  // 🔥 DELETE
  deleteTechnicien(id: number): Observable<{ message: string }> {
    return this.http
      .delete<{ status: string; data: { message: string } }>(`${this.baseUrl}techniciens/${id}`)
      .pipe(map(res => res.data));
  }

  // 🔥 ASSIGN NOTE
  assignNoteToTechnicien(technicienId: number, noteId: number): Observable<Technicien> {
    return this.http
      .put<{ status: string; data: Technicien }>(
        `${this.baseUrl}techniciens/${technicienId}/assign_note/${noteId}`, {}
      )
      .pipe(map(res => res.data));
  }

  // 🔥 UNASSIGN NOTE
  unassignNoteFromTechnicien(technicienId: number): Observable<Technicien> {
    return this.http
      .put<{ status: string; data: Technicien }>(
        `${this.baseUrl}techniciens/${technicienId}/unassign_note`, {}
      )
      .pipe(map(res => res.data));
  }
}
