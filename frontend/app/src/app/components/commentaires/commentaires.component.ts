import { Component, Input, OnInit } from '@angular/core';
import { CommentaireService, Commentaire } from '../../services/commentaire.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-commentaires',
  templateUrl: './commentaires.component.html',
  styleUrls: ['./commentaires.component.css']
})
export class CommentairesComponent implements OnInit {

  @Input() tacheId!: number;  // 👈 anciennement noteId

  commentaires: Commentaire[] = [];
  newComment: { contenu: string } = { contenu: '' };
  errorMessage = '';

  constructor(
    private api: CommentaireService,
    private auth: AuthService
  ) {}

  ngOnInit(): void {
    this.loadCommentaires();
  }

  // ---------------------------------------
  // 🔵 Charger les commentaires
  // ---------------------------------------
  loadCommentaires(): void {
    if (!this.tacheId) return;

    this.api.getCommentaires(this.tacheId).subscribe({
      next: data => this.commentaires = data,
      error: err => console.error('Erreur chargement commentaires:', err)
    });
  }

  // ---------------------------------------
  // 🟢 Ajouter un commentaire
  // ---------------------------------------
  addComment(): void {
    this.errorMessage = '';

    // Vérification contenu
    if (!this.newComment.contenu.trim()) {
      this.errorMessage = 'Veuillez écrire un commentaire.';
      return;
    }

    // Vérification utilisateur
    const userId = this.auth.getUserId();
    if (!userId) {
      this.errorMessage = 'Vous devez être connecté pour commenter.';
      return;
    }

    // Payload correct pour TÂCHES
    const payload: Commentaire = {
      contenu: this.newComment.contenu,
      auteur_id: userId,
      tache_id: this.tacheId               // 👈 ICI changement important
    };

    this.api.createCommentaire(this.tacheId, payload).subscribe({
      next: c => {
        this.commentaires.push(c);
        this.newComment.contenu = '';
      },
      error: err => {
        console.error(err);
        this.errorMessage = 'Impossible de poster le commentaire.';
      }
    });
  }
}
