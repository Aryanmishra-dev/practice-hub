import { categoriesApi, questionsApi } from "@/lib/api";

// Mock fetch
global.fetch = jest.fn();

describe("Categories API", () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockClear();
  });

  it("fetches all categories", async () => {
    const mockCategories = [
      {
        id: "epo",
        name: "ePO Server Administration",
        description: "Test category",
        icon: "file-text",
        question_count: 100,
      },
    ];

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockCategories,
    });

    const result = await categoriesApi.getAll();

    expect(result).toEqual(mockCategories);
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/categories"),
      expect.any(Object)
    );
  });

  it("handles API errors gracefully", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({ detail: "Server error" }),
    });

    await expect(categoriesApi.getAll()).rejects.toThrow();
  });
});

describe("Questions API", () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockClear();
  });

  it("fetches questions by category", async () => {
    const mockQuestions = [
      {
        id: "q1",
        question_text: "What is ePO?",
        options: ["A", "B", "C", "D"],
        category_id: "epo",
        difficulty: "easy",
      },
    ];

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockQuestions,
    });

    const result = await questionsApi.getByCategory("epo");

    expect(result).toEqual(mockQuestions);
  });

  it("supports difficulty filter", async () => {
    const mockQuestions = [];

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockQuestions,
    });

    await questionsApi.getByCategory("epo", { difficulty: "hard" });

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("difficulty=hard"),
      expect.any(Object)
    );
  });
});
