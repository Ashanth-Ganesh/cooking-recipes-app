import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FavoritesService } from '../../services/favorites.service';
import { AuthService } from '../../services/auth.service';
import { FavoriteRecipe } from '../../models/recipe.model';

@Component({
  selector: 'app-favorites',
  standalone: true,
  imports: [RouterLink, CommonModule],
  templateUrl: './favorites.component.html',
  styleUrl: './favorites.component.css',
})
export class FavoritesComponent implements OnInit {
  favorites: FavoriteRecipe[] = [];
  loading = true;
  error = '';
  removing: number | null = null;

  constructor(private favoritesService: FavoritesService, private auth: AuthService) {}

  ngOnInit(): void {
    this.favoritesService.load().subscribe({
      next: (favs) => {
        this.favorites = favs;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load favorites.';
        this.loading = false;
      },
    });

    this.favoritesService.favorites$.subscribe((favs) => {
      this.favorites = favs;
    });
  }

  remove(recipeId: number): void {
    this.removing = recipeId;
    this.favoritesService.remove(recipeId).subscribe({
      next: () => (this.removing = null),
      error: () => (this.removing = null),
    });
  }

  getImage(fav: FavoriteRecipe): string {
    return fav.image_url || 'https://via.placeholder.com/300x200?text=No+Image';
  }

  getUsername(): string {
    return this.auth.getCurrentUser()?.username || '';
  }
}
