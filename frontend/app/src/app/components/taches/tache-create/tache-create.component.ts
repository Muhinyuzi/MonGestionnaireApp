import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TacheService, TacheCreate, Tache, Utilisateur } from '../../../services/tache.service';
import { AuthService } from '../../../services/auth.service';
import DOMPurify from 'dompurify';
import { ToastService } from '../../../services/toast.service';
import { Location } from '@angular/common';

@Component({
  selector: 'app-tache-create',
  templateUrl: './tache-create.component.html',
  styleUrls: ['./tache-create.component.css']
})
export class TacheCreateComponent implements OnInit {

  newTache: TacheCreate = {
    titre: '',
    contenu: '',
    equipe: '',
    auteur_id: 0,
    categorie: '',
    priorite: ''
  };

  newFiles: File[] = [];
  currentUser?: Utilisateur;
  isSubmitting = false;

  constructor(
    private api: TacheService,
    private router: Router,
    private auth: AuthService,
    private toast: ToastService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.currentUser = this.auth.getUser();

    if (!this.currentUser) {
      this.toast.show("⚠️ Session expirée, veuillez vous reconnecter.", "error");
      this.router.navigate(['/login']);
      return;
    }

    this.newTache.equipe = this.currentUser?.equipe ?? '';
    this.newTache.auteur_id = this.currentUser?.id ?? 0;
  }

  handleFileInput(event: any) {
    const files: FileList = event.target.files;
    for (let i = 0; i < files.length; i++) {
      this.newFiles.push(files[i]);
    }
  }

  removeFile(index: number) {
    this.newFiles.splice(index, 1);
  }

  addTache(): void {
    if (!this.newTache.titre || !this.newTache.contenu || !this.newTache.categorie || !this.newTache.priorite) {
      this.toast.show("❗ Veuillez remplir tous les champs obligatoires.", "error");
      return;
    }

    this.newTache.contenu = DOMPurify.sanitize(this.newTache.contenu);
    this.isSubmitting = true;

    this.api.createTacheWithFiles(this.newTache, this.newFiles).subscribe({
      next: (tache: Tache) => {
        this.toast.show("✅ Tâche créée avec succès !", "success");
        this.router.navigate(['/taches', tache.id]);
      },
      error: () => {
        this.toast.show("❌ Erreur lors de la création de la tâche", "error");
        this.isSubmitting = false;
      }
    });
  }

  goBack(): void {
    this.location.back();
  }
}
