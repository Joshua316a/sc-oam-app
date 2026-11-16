import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { QualityCalculator } from "../QualityCalculator"
import axios from "axios"

describe("QualityCalculator", () => {
  beforeEach(() => {
    jest.spyOn(axios, "post").mockResolvedValueOnce({
      data: {
        base_quality: 0.5,
        resource_qualities: { element: 0.8 },
        resource_weights: { element: 1 },
        final_quality: 0.55,
      },
      status: 200,
    } as any)
  })

  it("calculates quality when user clicks Calculate", async () => {
    const user = userEvent.setup()
    render(<QualityCalculator blueprintId={1} onResult={} onError={} />)

    // Fill form fields
    await user.type(screen.getByLabelText("Resource type"), "element")
    await user.type(screen.getByLabelText("Quality selector"), "750")
    await user.click(screen.getByText("Calculate"))

    // Verify result displayed
    expect(screen.getByText("0.75")).toBeInTheDocument() // base_quality
    expect(screen.getByText("0.85")).toBeInTheDocument() // final_quality
  })
})
