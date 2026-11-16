import { render, screen } from "@testing-library/react"
import { BlueprintsList } from "../BlueprintList"

describe("BlueprintsList", () => {
  // --- Basic rendering ---

  it("renders heading and placeholder when no data", () => {
    render(<BlueprintsList />)

    expect(screen.getByRole("heading", { level: 2 })).toBeInTheDocument()
    expect(
      screen.getByText("No blueprints found. Add one using the navigation."),
    ).toBeInTheDocument()
  })

  // --- Mocked API integration ---

  beforeEach(() => {
    jest.spyOn(axios, "get").mockResolvedValueOnce({
      data: {
        data: [
          {
            id: 1,
            blueprint_id: "bp_001",
            bp_name: "Test Missile",
            category: "weapons",
            subcategory: "missiles",
            craft_type: "missile",
            output_item_name: "missile",
            quality_min: 500,
            quality_max: 800,
            craft_time_seconds: 30,
            ilg_label: "Weapons/Missiles",
            owner_handle: "",
            acquired_date: "",
            is_learned: false,
            notes: "",
            created_at: "",
            updated_at: "",
          },
        ],
        success: true,
        message: "",
      },
      status: 200,
    } as any)
  })

  it("fetches and displays blueprints", () => {
    render(<BlueprintsList />)

    expect(screen.getByRole("heading", { level: 2 })).toBeInTheDocument()
    expect(screen.getByText("Test Missile")).toBeInTheDocument()
  })

  // --- Error handling ---

  it("shows error when API fails", () => {
    jest.spyOn(axios, "get").mockRejectedValueOnce(new Error("Network error"))

    render(<BlueprintsList />)

    expect(screen.getByText("Network error")).toBeInTheDocument()
  })
})
