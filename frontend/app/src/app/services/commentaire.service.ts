import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

// ---------------- TYPES ----------------

export interface Utilisateur {
  id?: number;
  nom: string;
  email: string;
  equipe?: string;
  type?: string;
}

export interface Commentaire {
  id?: number;
  contenu: string;
  auteur_id: number;
  tache_id: number;     // 👈 important : plus note_id
  date?: string;
  auteur?: Utilisateur;
}

// ---------------- SERVICE ----------------

@Injectable({
  providedIn: 'root'
})
export class CommentaireService {

  //private baseUrl = 'http://127.0.0.1:8000/';
  //private baseUrl = 'https://mongestionnaireapp.onrender.com/';
  private baseUrl = `${environment.apiUrl}/`;

  constructor(private http: HttpClient) {}

  // ---------------------------------------
  // 🔵 Récupérer les commentaires d'une tâche
  // ---------------------------------------
  getCommentaires(tacheId: number): Observable<Commentaire[]> {
    if (tacheId == null) throw new Error('ID tâche manquant pour récupérer les commentaires');
    return this.http.get<Commentaire[]>(`${this.baseUrl}taches/${tacheId}/commentaires/`);
  }

  // ---------------------------------------
  // 🟢 Poster un commentaire sur une tâche
  // ---------------------------------------
  createCommentaire(tacheId: number, commentaire: Commentaire): Observable<Commentaire> {
    if (tacheId == null) throw new Error('ID tâche manquant pour créer un commentaire');
    return this.http.post<Commentaire>(`${this.baseUrl}taches/${tacheId}/commentaires/`, commentaire);
  }
}
