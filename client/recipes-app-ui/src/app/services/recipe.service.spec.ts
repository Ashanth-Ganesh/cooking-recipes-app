import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { HttpTestingController } from '@angular/common/http/testing';
import { RecipeService } from './recipe.service';
import { Recipe, SearchResult } from '../models/recipe.model';

const mockRecipe: Recipe = {
  id: 42,
  title: 'Spaghetti Bolognese',
  image: 'https://example.com/pasta.jpg',
  readyInMinutes: 45,
  servings: 4,
  cuisines: ['Italian'],
  dishTypes: ['main course'],
  diets: [],
};

const mockSearchResult: SearchResult = {
  results: [mockRecipe],
  offset: 0,
  number: 1,
  totalResults: 1,
};

describe('RecipeService', () => {
  let service: RecipeService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [RecipeService, provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(RecipeService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('search', () => {
    it('GETs the search endpoint', () => {
      service.search({}).subscribe();
      const req = httpMock.expectOne((r) => r.url === 'http://localhost:8000/api/recipes/search');
      expect(req.request.method).toBe('GET');
      req.flush(mockSearchResult);
    });

    it('sends query param when provided', () => {
      service.search({ query: 'pasta' }).subscribe();
      const req = httpMock.expectOne((r) => r.url.includes('/search'));
      expect(req.request.params.get('query')).toBe('pasta');
      req.flush(mockSearchResult);
    });

    it('sends cuisine param when provided', () => {
      service.search({ cuisine: 'Italian' }).subscribe();
      const req = httpMock.expectOne((r) => r.url.includes('/search'));
      expect(req.request.params.get('cuisine')).toBe('Italian');
      req.flush(mockSearchResult);
    });

    it('sends diet param when provided', () => {
      service.search({ diet: 'vegan' }).subscribe();
      const req = httpMock.expectOne((r) => r.url.includes('/search'));
      expect(req.request.params.get('diet')).toBe('vegan');
      req.flush(mockSearchResult);
    });

    it('sends max_ready_time param when provided', () => {
      service.search({ max_ready_time: 30 }).subscribe();
      const req = httpMock.expectOne((r) => r.url.includes('/search'));
      expect(req.request.params.get('max_ready_time')).toBe('30');
      req.flush(mockSearchResult);
    });

    it('does not send max_ready_time when null', () => {
      service.search({ max_ready_time: null }).subscribe();
      const req = httpMock.expectOne((r) => r.url.includes('/search'));
      expect(req.request.params.has('max_ready_time')).toBe(false);
      req.flush(mockSearchResult);
    });

    it('sends number and offset params', () => {
      service.search({ number: 24, offset: 12 }).subscribe();
      const req = httpMock.expectOne((r) => r.url.includes('/search'));
      expect(req.request.params.get('number')).toBe('24');
      expect(req.request.params.get('offset')).toBe('12');
      req.flush(mockSearchResult);
    });

    it('returns the search result', () => {
      let result: SearchResult | undefined;
      service.search({ query: 'chicken' }).subscribe((r) => (result = r));
      const req = httpMock.expectOne((r) => r.url.includes('/search'));
      req.flush(mockSearchResult);
      expect(result).toEqual(mockSearchResult);
    });
  });

  describe('getById', () => {
    it('GETs the correct recipe endpoint', () => {
      service.getById(42).subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/recipes/42');
      expect(req.request.method).toBe('GET');
      req.flush(mockRecipe);
    });

    it('returns the recipe', () => {
      let result: Recipe | undefined;
      service.getById(42).subscribe((r) => (result = r));
      const req = httpMock.expectOne('http://localhost:8000/api/recipes/42');
      req.flush(mockRecipe);
      expect(result).toEqual(mockRecipe);
    });
  });

  describe('getCustomRecipes', () => {
    it('GETs the custom recipes endpoint', () => {
      service.getCustomRecipes().subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/recipes/custom');
      expect(req.request.method).toBe('GET');
      req.flush(mockSearchResult);
    });

    it('returns the search result', () => {
      let result: SearchResult | undefined;
      service.getCustomRecipes().subscribe((r) => (result = r));
      const req = httpMock.expectOne('http://localhost:8000/api/recipes/custom');
      req.flush(mockSearchResult);
      expect(result).toEqual(mockSearchResult);
    });
  });

  describe('searchByIngredients', () => {
    it('GETs the by-ingredients endpoint', () => {
      service.searchByIngredients('tomato,garlic').subscribe();
      const req = httpMock.expectOne((r) => r.url.includes('/by-ingredients'));
      expect(req.request.method).toBe('GET');
      req.flush([mockRecipe]);
    });

    it('sends ingredients and default number params', () => {
      service.searchByIngredients('tomato,garlic').subscribe();
      const req = httpMock.expectOne((r) => r.url.includes('/by-ingredients'));
      expect(req.request.params.get('ingredients')).toBe('tomato,garlic');
      expect(req.request.params.get('number')).toBe('12');
      req.flush([]);
    });

    it('sends custom number param when provided', () => {
      service.searchByIngredients('chicken', 6).subscribe();
      const req = httpMock.expectOne((r) => r.url.includes('/by-ingredients'));
      expect(req.request.params.get('number')).toBe('6');
      req.flush([]);
    });
  });
});
