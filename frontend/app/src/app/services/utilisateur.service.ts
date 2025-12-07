// src/app/services/utilisateur.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, map } from 'rxjs';

// ---------------- TYPES ----------------
export interface Utilisateur {
  id?: number;
  nom: string;
  email: string;
  mot_de_passe?: string;
  equipe?: string;
  type?: string;
  poste?: string;
  telephone?: string;
  adresse?: string;
  date_embauche?: string;
  is_active?: boolean;
  avatar_url?: string;
}

export interface Tache {
  id: number;
  titre: string;
  contenu: string;
  equipe?: string;
  created_at: string;
  updated_at?: string;
  auteur_id: number;
  auteur?: Utilisateur;
  fichiers?: any[];
  commentaires?: any[];
  assign_to_id?: number | null;
  categorie?: string;
  priorite?: string;
  status?: string;
}

export interface Commentaire {
  id?: number;
  contenu: string;
  auteur_id: number;
  tache_id: number;
  date?: string;
  auteur?: Utilisateur;
}

export interface UtilisateurDetailOut extends Utilisateur {
  date?: string;
  taches?: Tache[];          // Tâches créées
  assignations?: Tache[];    // Tâches assignées
  commentaires?: Commentaire[];
}

export interface PaginatedUsers {
  total: number;
  page: number;
  limit: number;
  users: Utilisateur[];
}

// ---------------- SERVICE ----------------
@Injectable({
  providedIn: 'root'
})
export class UtilisateurService {

  //private baseUrl = 'http://127.0.0.1:8000/';
  private baseUrl = 'https://mongestionnaireapp.onrender.com/';


  constructor(private http: HttpClient) {}

  // --------------------------------------------------
  //             CRUD UTILISATEURS
  // --------------------------------------------------

  getUtilisateurs(page: number = 1, limit: number = 10): Observable<PaginatedUsers> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('limit', limit.toString());

    return this.http
      .get<{ status: string; data: PaginatedUsers }>(`${this.baseUrl}utilisateurs/`, { params })
      .pipe(map(res => res.data));
  }

  createUtilisateur(user: Utilisateur): Observable<Utilisateur> {
    return this.http
      .post<{ status: string; data: Utilisateur }>(`${this.baseUrl}utilisateurs/`, user)
      .pipe(map(res => res.data));
  }

  getUtilisateurDetail(id: number): Observable<UtilisateurDetailOut> {
    return this.http
      .get<{ status: string; data: UtilisateurDetailOut }>(`${this.baseUrl}utilisateurs/${id}`)
      .pipe(map(res => res.data));
  }

  updateUtilisateur(userId: number, userData: Partial<Utilisateur>): Observable<Utilisateur> {
    return this.http
      .put<{ status: string; data: Utilisateur }>(`${this.baseUrl}utilisateurs/${userId}`, userData)
      .pipe(map(res => res.data));
  }

  deleteUtilisateur(userId: number): Observable<string> {
    return this.http
      .delete<{ status: string; data: { message: string } }>(`${this.baseUrl}utilisateurs/${userId}`)
      .pipe(map(res => res.data.message));
  }

  // --------------------------------------------------
  //                     AVATARS
  // --------------------------------------------------

  uploadAvatar(userId: number, formData: FormData) {
    return this.http
      .post<{ status: string; data: any }>(`${this.baseUrl}utilisateurs/${userId}/avatar`, formData)
      .pipe(map(res => res.data));
  }

  getAvatar(userId: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}utilisateurs/${userId}/avatar`, {
      responseType: 'blob'
    });
  }

  getDefaultAvatarUrl(): string {
    return `${this.baseUrl}avatars/default`;
  }

  // --------------------------------------------------
  //             GESTION DES TÂCHES (ALIGNÉ AU BACKEND)
  // --------------------------------------------------

  /** Assigner une tâche à un utilisateur */
  assignTacheToUser(userId: number, tacheId: number) {
    return this.http
      .post<{ status: string; data: any }>(
        `${this.baseUrl}utilisateurs/${userId}/assign-tache/${tacheId}`,
        {}
      )
      .pipe(map(res => res.data));
  }

  /** Désassigner une tâche d’un utilisateur */
  unassignTacheFromUser(userId: number, tacheId: number) {
    return this.http
      .post<{ status: string; data: any }>(
        `${this.baseUrl}utilisateurs/${userId}/unassign-tache/${tacheId}`,
        {}
      )
      .pipe(map(res => res.data));
  }

  /** Clôturer une tâche (status = terminé) */
  closeTache(userId: number, tacheId: number) {
    return this.http
      .post<{ status: string; data: any }>(
        `${this.baseUrl}utilisateurs/${userId}/close-tache/${tacheId}`,
        {}
      )
      .pipe(map(res => res.data));
  }

}
