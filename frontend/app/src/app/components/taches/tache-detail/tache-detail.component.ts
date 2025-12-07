import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TacheService, Tache, Utilisateur } from '../../../services/tache.service';
import { AuthService } from '../../../services/auth.service';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../shared/confirm-dialog/confirm-dialog.component';
import { ToastService } from '../../../services/toast.service';

@Component({
  selector: 'app-tache-detail',
  templateUrl: './tache-detail.component.html',
  styleUrls: ['./tache-detail.component.css']
})
export class TacheDetailComponent implements OnInit {
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  tache?: Tache;
  utilisateur?: Utilisateur;
  isLoading = true;
  errorMessage = '';
  isEditing = false;
  hasLiked = false;

  newFiles: File[] = [];
  currentUser?: Utilisateur;

  constructor(
    private route: ActivatedRoute,
    private api: TacheService,
    private router: Router,
    private dialog: MatDialog,
    private auth: AuthService,
    private toast: ToastService,
  ) {}

  ngOnInit(): void {
    this.currentUser = this.auth.getUser();

    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.api.getTacheById(id).subscribe({
      next: (data) => {
        this.tache = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = "❌ Impossible de charger la tâche.";
        this.isLoading = false;
        this.toast.show(this.errorMessage, "error");
      }
    });
  }

  handleFileInput(event: any) {
    const files: FileList = event.target.files;
    for (let i = 0; i < files.length; i++) this.newFiles.push(files[i]);

    if (this.tache) {
      this.tache.fichiers = this.tache.fichiers || [];
      this.tache.fichiers.push(...Array.from(files).map((file, i) => ({
        id: Date.now() + i,
        nom_fichier: file.name,
        chemin: ''
      })));
    }
  }

  removeFile(index: number) {
    this.newFiles.splice(index, 1);
  }

  updateTache(): void {
    if (!this.tache) return;

    const formData = new FormData();
    formData.append('titre', this.tache.titre);
    formData.append('contenu', this.tache.contenu);
    if (this.tache.equipe) formData.append('equipe', this.tache.equipe);
    if (this.tache.priorite) formData.append('priorite', this.tache.priorite);
    if (this.tache.categorie) formData.append('categorie', this.tache.categorie);

    this.newFiles.forEach(file => formData.append('fichiers', file));

    this.api.updateTacheWithFiles(this.tache.id, this.tache, this.newFiles).subscribe({
      next: () => {
        this.isEditing = false;
        this.newFiles = [];
        this.toast.show("✅ Tâche mise à jour avec succès !", "success");
      },
      error: () => {
        this.toast.show("❌ Erreur lors de la mise à jour", "error");
      }
    });
  }

  deleteTache(): void {
    if (!this.tache) return;

    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '350px',
      data: { message: "Voulez-vous vraiment supprimer cette tâche ?" }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.api.deleteTache(this.tache!.id).subscribe({
          next: () => {
            this.toast.show("✅ Tâche supprimée", "success");
            this.router.navigate(['/taches']);
          },
          error: () => {
            this.toast.show("❌ Erreur lors de la suppression", "error");
          }
        });
      }
    });
  }

  canEditOrDelete(tache: Tache): boolean {
    return this.currentUser?.id === tache.auteur?.id || this.currentUser?.type === 'admin';
  }

  likeTache(): void {
    if (!this.tache || this.hasLiked) return;

    this.api.likeTache(this.tache.id).subscribe({
      next: res => {
        if (this.tache) this.tache.likes = res.likes;
        this.hasLiked = true;
      },
      error: () => {
        this.toast.show("❌ Erreur lors du like", "error");
      }
    });
  }

  getFileUrl(path: string): string {
    const fixedPath = path.replace(/\\/g, '/');
    return `${this.api.getBaseUrl()}${fixedPath}`;
  }

  viewImage(path: string) {
    window.open(this.getFileUrl(path), '_blank');
  }

  isNew(dateStr: string): boolean {
    const created = new Date(dateStr);
    const now = new Date();
    const diff = (now.getTime() - created.getTime()) / (1000*60*60*24);
    return diff <= 7;
  }

  removeExistingFile(fichierId: number) {
    if (!this.tache) return;

    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '350px',
      data: { message: "Voulez-vous vraiment supprimer ce fichier ?" }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.api.deleteFile(fichierId).subscribe({
          next: () => {
            this.tache!.fichiers = this.tache!.fichiers?.filter(f => f.id !== fichierId);
            this.toast.show("✅ Fichier supprimé", "success");
          },
          error: () => {
            this.toast.show("❌ Erreur lors de la suppression du fichier", "error");
          }
        });
      }
    });
  }
}
