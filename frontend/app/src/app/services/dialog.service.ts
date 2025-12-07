import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../components/shared/confirm-dialog/confirm-dialog.component';

@Injectable({ providedIn: 'root' })
export class DialogService {
  constructor(private dialog: MatDialog) {}

  /** 🔹 Fenêtre Oui / Non */
  confirm(title: string, message: string) {
    return this.dialog.open(ConfirmDialogComponent, {
      width: '380px',
      data: {
        title,
        message,
        mode: 'confirm'       // mode par défaut
      }
    }).afterClosed();
  }

  /** 🔹 Fenêtre OK seulement (alert) */
  alert(title: string, message: string) {
    return this.dialog.open(ConfirmDialogComponent, {
      width: '380px',
      data: {
        title,
        message,
        mode: 'alert'        // 👈 très important
      }
    }).afterClosed();
  }
}
