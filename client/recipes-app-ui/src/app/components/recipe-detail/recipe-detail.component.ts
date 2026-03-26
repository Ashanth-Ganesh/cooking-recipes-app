import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RecipeService } from '../../services/recipe.service';
import { FavoritesService } from '../../services/favorites.service';
import { AuthService } from '../../services/auth.service';
import { Recipe } from '../../models/recipe.model';

@Component({
  selector: 'app-recipe-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './recipe-detail.component.html',
  styleUrl: './recipe-detail.component.css',
})
export class RecipeDetailComponent implements OnInit {
  recipe: Recipe | null = null;
  loading = true;
  error = '';
  isSaved = false;
  saving = false;
  isLoggedIn = false;
  activeTab: 'ingredients' | 'instructions' | 'nutrition' = 'ingredients';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private recipeService: RecipeService,
    private favorites: FavoritesService,
    private auth: AuthService
  ) {}

  ngOnInit(): void {
    this.isLoggedIn = this.auth.isLoggedIn();
    if (this.isLoggedIn) {
      this.favorites.load().subscribe();
    }
    const id = +this.route.snapshot.paramMap.get('id')!;
    this.recipeService.getById(id).subscribe({
      next: (recipe) => {
        this.recipe = recipe;
        this.loading = false;
        this.favorites.favorites$.subscribe(() => {
          if (recipe) this.isSaved = this.favorites.isSaved(recipe.id);
        });
      },
      error: () => {
        this.error = 'Recipe not found or failed to load.';
        this.loading = false;
      },
    });
  }

  toggleFavorite(): void {
    if (!this.recipe || !this.isLoggedIn || this.saving) return;
    this.saving = true;

    if (this.isSaved) {
      const recipeId = this.favorites.getFavoriteRecipeId(this.recipe.id);
      if (recipeId) {
        this.favorites.remove(recipeId).subscribe({ complete: () => (this.saving = false) });
      } else {
        this.saving = false;
      }
    } else {
      this.favorites.save(this.recipe).subscribe({ complete: () => (this.saving = false) });
    }
  }

  stripHtml(html: string): string {
    return html.replace(/<[^>]*>/g, '');
  }

  getInstructions(): string[] {
    if (!this.recipe?.instructions) return [];
    return this.recipe.instructions
      .split(/\n+/)
      .map((s) => s.trim())
      .filter((s) => s.length > 0);
  }

  getCalories(): number | null {
    if (!this.recipe?.nutrition?.nutrients) return null;
    const cal = this.recipe.nutrition.nutrients.find((n) => n.name === 'Calories');
    return cal ? Math.round(cal.amount) : null;
  }

  getKeyNutrients() {
    if (!this.recipe?.nutrition?.nutrients) return [];
    const keys = ['Protein', 'Fat', 'Carbohydrates', 'Fiber', 'Sugar', 'Sodium'];
    return this.recipe.nutrition.nutrients
      .filter((n) => keys.includes(n.name))
      .slice(0, 6);
  }

  getDietBadges(): string[] {
    const badges: string[] = [];
    if (this.recipe?.vegetarian) badges.push('Vegetarian');
    if (this.recipe?.vegan) badges.push('Vegan');
    if (this.recipe?.glutenFree) badges.push('Gluten-Free');
    if (this.recipe?.dairyFree) badges.push('Dairy-Free');
    if (this.recipe?.cheap) badges.push('Budget-Friendly');
    return badges;
  }
}
