import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Recipe } from '../../models/recipe.model';
import { AuthService } from '../../services/auth.service';
import { FavoritesService } from '../../services/favorites.service';

@Component({
  selector: 'app-recipe-card',
  standalone: true,
  imports: [RouterLink, CommonModule],
  templateUrl: './recipe-card.component.html',
  styleUrl: './recipe-card.component.css',
})
export class RecipeCardComponent implements OnInit {
  @Input() recipe!: Recipe;
  @Output() favoriteToggled = new EventEmitter<Recipe>();

  isSaved = false;
  isLoggedIn = false;
  saving = false;

  constructor(private auth: AuthService, private favorites: FavoritesService) {}

  ngOnInit(): void {
    this.isLoggedIn = this.auth.isLoggedIn();
    this.favorites.favorites$.subscribe(() => {
      this.isSaved = this.favorites.isSaved(this.recipe.id);
    });
  }

  toggleFavorite(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    if (!this.isLoggedIn || this.saving) return;

    this.saving = true;
    if (this.isSaved) {
      const recipeId = this.favorites.getFavoriteRecipeId(this.recipe.id);
      if (recipeId) {
        this.favorites.remove(recipeId).subscribe({
          next: () => (this.saving = false),
          error: () => (this.saving = false),
        });
      } else {
        this.saving = false;
      }
    } else {
      this.favorites.save(this.recipe).subscribe({
        next: () => (this.saving = false),
        error: () => (this.saving = false),
      });
    }
  }

  getDietTags(): string[] {
    const tags: string[] = [];
    if (this.recipe.vegetarian) tags.push('Vegetarian');
    if (this.recipe.vegan) tags.push('Vegan');
    if (this.recipe.glutenFree) tags.push('Gluten-Free');
    if (this.recipe.dairyFree) tags.push('Dairy-Free');
    return tags.slice(0, 2);
  }

  getImageUrl(): string {
    return this.recipe.image || 'https://spoonacular.com/recipeImages/default-food.jpg';
  }
}
