import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

/* -------------------------------
        INTERFACES
-------------------------------- */

// ---------- Utilisateur ----------
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
}

export interface UtilisateurDetailOut extends Utilisateur {
  id: number;
  date?: string;
  taches: Tache[];
  commentaires: Commentaire[];
}

// ---------- Pagination utilisateurs ----------
export interface UtilisateursResponse {
  total: number;
  page: number;
  limit: number;
  users: Utilisateur[];
}

// ---------- Fichier associé ----------
export interface FichierTache {
  id: number;
  nom_fichier: string;
  chemin: string;
}

// ---------- Commentaire ----------
export interface Commentaire {
  id?: number;
  contenu: string;
  auteur_id: number;
  tache_id: number;
  date?: string;
  auteur?: Utilisateur;
}

// ---------- Tâche ----------
export interface Tache {
  id: number;
  titre: string;
  contenu: string;
  equipe?: string;
  created_at: string;
  updated_at?: string;
  auteur_id: number;
  auteur?: Utilisateur;
  assign_to?: Utilisateur;
  commentaires: Commentaire[];
  fichiers?: FichierTache[];

  // Champs additionnels backend
  nb_vues?: number;
  likes?: number;
  resume_ia?: string;
  categorie?: string;
  priorite?: string;
}

// ---------- Création tâche ----------
export interface TacheCreate {
  titre: string;
  contenu: string;
  equipe?: string;
  auteur_id: number;
  priorite?: string;
  categorie?: string;
}

// ---------- Pagination tâches ----------
export interface TachesResponse {
  total?: number;
  page?: number;
  limit?: number;
  taches: Tache[];
}

/* -------------------------------
          SERVICE TÂCHES
-------------------------------- */

@Injectable({
  providedIn: 'root'
})
export class TacheService {

  //private baseUrl = 'http://127.0.0.1:8000/';
  private baseUrl = 'https://mongestionnaireapp.onrender.com/';


  constructor(private http: HttpClient) {}

  getBaseUrl(): string {
    return this.baseUrl;
  }

  /* --------------------------------------------
      TÂCHES : LISTE / DETAIL
  --------------------------------------------- */

  /** Liste paginée et filtrée des tâches */
  getTaches(
    search?: string,
    author?: string,
    assign_to?: number,                                  // 🔥 AJOUT ICI
    sort: 'date_asc' | 'date_desc' = 'date_desc',
    page: number = 1,
    limit: number = 10
  ): Observable<TachesResponse> {

    let params = new HttpParams()
      .set('sort', sort)
      .set('page', page.toString())
      .set('limit', limit.toString());

    if (search) params = params.set('search', search);
    if (author) params = params.set('author', author);
    if (assign_to) params = params.set('assign_to', assign_to.toString());   // 🔥 AJOUT ICI

    return this.http.get<TachesResponse>(`${this.baseUrl}taches/`, { params });
  }

  /** Détail d'une tâche */
  getTacheById(id: number): Observable<Tache> {
    if (id == null) throw new Error('ID tâche manquant');
    return this.http.get<Tache>(`${this.baseUrl}taches/${id}/`);
  }

  /* --------------------------------------------
            CRÉATION TÂCHE
  --------------------------------------------- */

  /** Crée une tâche simple */
  createTache(tache: TacheCreate): Observable<Tache> {
    return this.http.post<Tache>(`${this.baseUrl}taches/`, tache);
  }

  /** Crée une tâche avec fichiers */
  createTacheWithFiles(tache: TacheCreate, files: File[]): Observable<Tache> {
    const formData = new FormData();
    formData.append('titre', tache.titre);
    formData.append('contenu', tache.contenu);
    formData.append('auteur_id', tache.auteur_id.toString());
    if (tache.equipe) formData.append('equipe', tache.equipe);
    if (tache.priorite) formData.append('priorite', tache.priorite);
    if (tache.categorie) formData.append('categorie', tache.categorie);

    files.forEach(file => formData.append('fichiers', file));

    return this.http.post<Tache>(`${this.baseUrl}taches/`, formData);
  }

  /* --------------------------------------------
             UPDATE TÂCHE
  --------------------------------------------- */

  updateTache(id: number, tache: Partial<Tache>): Observable<Tache> {
    if (id == null) throw new Error('ID tâche manquant');
    return this.http.put<Tache>(`${this.baseUrl}taches/${id}/`, tache);
  }

  updateTacheWithFiles(id: number, tache: TacheCreate, files: File[]): Observable<Tache> {
    if (id == null) throw new Error('ID tâche manquant');

    const formData = new FormData();
    formData.append('titre', tache.titre);
    formData.append('contenu', tache.contenu);
    formData.append('auteur_id', tache.auteur_id.toString());
    if (tache.equipe) formData.append('equipe', tache.equipe);
    if (tache.priorite) formData.append('priorite', tache.priorite);
    if (tache.categorie) formData.append('categorie', tache.categorie);

    files.forEach(file => formData.append('fichiers', file));

    return this.http.put<Tache>(`${this.baseUrl}taches/${id}/`, formData);
  }

  /* --------------------------------------------
              DELETE TÂCHE
  --------------------------------------------- */

  deleteTache(id: number): Observable<void> {
    if (id == null) throw new Error('ID tâche manquant');
    return this.http.delete<void>(`${this.baseUrl}taches/${id}/`);
  }

  /* --------------------------------------------
                 LIKE TÂCHE
  --------------------------------------------- */

  likeTache(id: number): Observable<{ likes: number }> {
    if (id == null) throw new Error('ID tâche manquant');
    return this.http.post<{ likes: number }>(`${this.baseUrl}taches/${id}/like`, {});
  }

  /* --------------------------------------------
                COMMENTAIRES
  --------------------------------------------- */

  getCommentaires(tacheId: number): Observable<Commentaire[]> {
    if (tacheId == null) throw new Error('ID tâche manquant');
    return this.http.get<Commentaire[]>(`${this.baseUrl}taches/${tacheId}/commentaires`);
  }

  addCommentaire(tacheId: number, commentaire: Commentaire): Observable<Commentaire> {
    if (tacheId == null) throw new Error('ID tâche manquant');
    return this.http.post<Commentaire>(`${this.baseUrl}taches/${tacheId}/commentaires`, commentaire);
  }

  /* --------------------------------------------
                  FICHIERS
  --------------------------------------------- */

  deleteFile(fileId: number): Observable<{ detail: string }> {
    if (fileId == null) throw new Error('ID fichier manquant');
    return this.http.delete<{ detail: string }>(`${this.baseUrl}taches/fichiers/${fileId}`);
  }

}
