/**
 * POST /api/knowledge
 * { topic: string, angle?: string }
 * → { formulas: [...], misconceptions: [...], summary: string }
 *
 * For 10 demo topics: returns hardcoded static content instantly (no Groq).
 * For all other topics: calls Groq.
 */
import { Router } from "express";
import Groq from "groq-sdk";

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
export const knowledgeRoute = Router();

// ── Hardcoded static knowledge for 10 demo topics ─────────────────────────
const STATIC_KNOWLEDGE = {
  "eigenvalues and eigenvectors": {
    formulas: [
      { formula: "Av = λv", meaning: "A matrix A acting on eigenvector v just scales it by eigenvalue λ — no rotation, pure stretching" },
      { formula: "det(A − λI) = 0", meaning: "The characteristic equation — set this to find all eigenvalues of A" },
      { formula: "tr(A) = λ₁ + λ₂ + … + λₙ", meaning: "The trace of A (sum of diagonal) equals the sum of all its eigenvalues" },
      { formula: "det(A) = λ₁ × λ₂ × … × λₙ", meaning: "The determinant of A equals the product of all its eigenvalues" },
      { formula: "(A − λI)v = 0", meaning: "After finding λ, solve this system to find the corresponding eigenvectors" },
    ],
    misconceptions: [
      { wrong: "Every matrix has real eigenvalues", correct: "Rotation matrices have complex eigenvalues; real eigenvalues are only guaranteed for symmetric matrices" },
      { wrong: "Eigenvectors change direction when multiplied by the matrix", correct: "Eigenvectors are exactly those that don't change direction — they only scale by λ" },
      { wrong: "A matrix with n rows always has n distinct eigenvectors", correct: "Only diagonalizable matrices have n linearly independent eigenvectors; defective matrices have repeated eigenvalues with fewer independent eigenvectors" },
      { wrong: "Eigenvalues are always positive", correct: "Eigenvalues can be negative (reflection), zero (singular matrix), or complex (rotation)" },
    ],
    summary: "• Eigenvectors are the special directions a transformation leaves unchanged — only scaling occurs\n• The characteristic equation det(A − λI) = 0 yields the eigenvalues\n• The trace of A equals the sum of eigenvalues; the determinant equals their product\n• Diagonalization rewrites A as PDP⁻¹, making repeated powers trivial: Aⁿv = λⁿv\n• Eigendecomposition powers PCA, Google PageRank, quantum mechanics, and differential equations",
  },

  "derivatives": {
    formulas: [
      { formula: "f′(x) = lim(h→0) [f(x+h) − f(x)] / h", meaning: "The derivative is the limit of the secant slope as the gap shrinks to zero — instantaneous rate of change" },
      { formula: "d/dx [xⁿ] = nxⁿ⁻¹", meaning: "Power rule: bring the exponent down and reduce it by one" },
      { formula: "d/dx [eˣ] = eˣ", meaning: "The exponential function is its own derivative — unique among all functions" },
      { formula: "d/dx [sin x] = cos x", meaning: "The slope of the sine wave follows the cosine wave exactly" },
      { formula: "d/dx [ln x] = 1/x", meaning: "The log's rate of change shrinks as x grows — it slows down logarithmically" },
    ],
    misconceptions: [
      { wrong: "The derivative is just rise over run", correct: "It's the instantaneous rate of change — a limit, not a simple slope between two points" },
      { wrong: "A continuous function is always differentiable", correct: "Continuity doesn't guarantee differentiability — |x| is continuous but not differentiable at x = 0" },
      { wrong: "d/dx means you divide by dx", correct: "dx is not a number; it's notation for the limiting process — infinitesimally small but never actually zero" },
      { wrong: "Setting f′(x) = 0 always finds a maximum or minimum", correct: "It finds candidates — you must check the second derivative or compare values to confirm a max or min" },
    ],
    summary: "• The derivative measures instantaneous rate of change — the slope of the tangent line at a single point\n• Standard rules (power, product, quotient, chain) let you differentiate without computing limits each time\n• Derivatives are zero at local maxima and minima — crucial for optimization\n• The second derivative tells you concavity — whether the function is curving up or down\n• Derivatives underpin physics (velocity/acceleration), machine learning (gradient descent), and economics (marginal cost/revenue)",
  },

  "gradient descent": {
    formulas: [
      { formula: "θ ← θ − α∇L(θ)", meaning: "Update rule: move parameters opposite to the gradient by step size α (the learning rate)" },
      { formula: "∇L(θ) = [∂L/∂θ₁, ∂L/∂θ₂, …]", meaning: "The gradient is a vector of partial derivatives — it points uphill, so we move opposite to it" },
      { formula: "L(θ) = (1/n) Σ (ŷᵢ − yᵢ)²", meaning: "Mean squared error loss — the landscape we're descending; lower is better" },
      { formula: "α (learning rate)", meaning: "Controls step size: too large diverges, too small converges very slowly — must be tuned carefully" },
    ],
    misconceptions: [
      { wrong: "Gradient descent always finds the global minimum", correct: "It finds a local minimum; global minimum is only guaranteed for convex (bowl-shaped) loss surfaces" },
      { wrong: "A smaller learning rate is always better", correct: "Too small means extremely slow convergence or getting stuck; it must be balanced against stability" },
      { wrong: "The gradient points toward the minimum", correct: "The gradient points uphill (steepest ascent); we move opposite to it to descend" },
      { wrong: "One pass of gradient descent is enough", correct: "Many iterations over the data are needed; convergence depends on the loss landscape and learning rate" },
    ],
    summary: "• Gradient descent iteratively moves parameters downhill on the loss surface using the negative gradient\n• The learning rate controls step size and must be tuned — adaptive methods like Adam adjust it automatically\n• Stochastic and mini-batch variants use subsets of data for faster, noisier updates\n• It converges to a local minimum; convex problems guarantee the global minimum\n• It is the engine behind training virtually every modern neural network",
  },

  "linear transformations": {
    formulas: [
      { formula: "T(u + v) = T(u) + T(v)", meaning: "Additivity: transforming a sum equals the sum of transformations — addition is preserved" },
      { formula: "T(cv) = cT(v)", meaning: "Homogeneity: scaling then transforming equals transforming then scaling — scalar multiplication is preserved" },
      { formula: "T(v) = Av", meaning: "Every linear transformation between finite-dimensional spaces is represented by matrix multiplication" },
      { formula: "Columns of A = images of basis vectors", meaning: "The columns of the matrix tell you exactly where each basis vector lands after the transformation" },
    ],
    misconceptions: [
      { wrong: "Linear means the output graph is a straight line", correct: "Linear means preserving addition and scalar multiplication — a rotation is linear even though it isn't a line" },
      { wrong: "Composition of transformations is commutative", correct: "Matrix multiplication is not commutative — T₁ followed by T₂ generally differs from T₂ followed by T₁" },
      { wrong: "Translation (sliding everything in one direction) is a linear transformation", correct: "Translation breaks additivity — T(0) ≠ 0 — so it is not linear; it requires affine or homogeneous coordinates" },
      { wrong: "All matrices represent the same kind of transformation", correct: "Matrices encode rotations, reflections, shears, projections, and scalings — each geometrically distinct" },
    ],
    summary: "• Linear transformations preserve vector addition and scalar multiplication — they are the structure-preserving maps of linear algebra\n• Every linear transformation between finite-dimensional spaces is represented by a matrix\n• The columns of the matrix are the images of the basis vectors — no memorization needed, just track where bases land\n• Composition of transformations corresponds to matrix multiplication — applied right to left\n• They are the mathematical language of computer graphics, robotics, machine learning, and physics",
  },

  "determinants": {
    formulas: [
      { formula: "det([[a,b],[c,d]]) = ad − bc", meaning: "For a 2×2 matrix: the signed area of the parallelogram formed by the two column vectors" },
      { formula: "det(AB) = det(A) · det(B)", meaning: "The determinant of a product is the product of determinants — it's multiplicative" },
      { formula: "det(A) = 0 ⟺ A is singular", meaning: "Zero determinant means the transformation collapses space to a lower dimension — no inverse exists" },
      { formula: "det(Aᵀ) = det(A)", meaning: "Transposing a matrix doesn't change its determinant" },
      { formula: "det(A⁻¹) = 1/det(A)", meaning: "The inverse matrix has the reciprocal determinant — it undoes the scaling" },
    ],
    misconceptions: [
      { wrong: "The determinant is just a computational formula", correct: "The determinant measures the signed volume scaling of the transformation — it has deep geometric meaning" },
      { wrong: "Negative determinant means something went wrong", correct: "Negative determinant means the transformation includes a reflection — orientation is flipped, which is valid and meaningful" },
      { wrong: "Row operations don't change the determinant", correct: "Swapping rows flips the sign; scaling a row by c multiplies the determinant by c; only adding a multiple of one row to another leaves it unchanged" },
      { wrong: "A nonzero determinant just means the matrix is invertible", correct: "The actual value tells you by how much volumes are scaled — det = 3 means all volumes are tripled" },
    ],
    summary: "• The determinant measures how much a linear transformation scales areas (2D) or volumes (3D)\n• Zero determinant means the transformation collapses space — no inverse exists\n• The sign encodes orientation: positive preserves it, negative flips it (a reflection occurred)\n• det(AB) = det(A)det(B) makes it multiplicative and useful in change-of-variables calculus\n• Eigenvalues come from the characteristic equation det(A − λI) = 0 — the determinant is central to eigenanalysis",
  },

  "backpropagation": {
    formulas: [
      { formula: "∂L/∂w = ∂L/∂a · ∂a/∂z · ∂z/∂w", meaning: "Chain rule applied layer by layer — the gradient of loss w.r.t. each weight is a product of local derivatives" },
      { formula: "δˡ = (Wˡ⁺¹)ᵀδˡ⁺¹ ⊙ σ′(zˡ)", meaning: "Error signal at layer l: backpropagated error from the next layer times the local activation derivative" },
      { formula: "w ← w − α · ∂L/∂w", meaning: "Gradient descent update: move each weight opposite its gradient, scaled by the learning rate" },
      { formula: "∂L/∂b = δˡ", meaning: "Bias gradient equals the error signal at that layer — a direct consequence of the chain rule" },
    ],
    misconceptions: [
      { wrong: "Backpropagation is a learning algorithm", correct: "Backprop only computes gradients — gradient descent uses those gradients to actually update weights and learn" },
      { wrong: "Backpropagation recomputes all derivatives from scratch each time", correct: "It caches intermediate values from the forward pass and reuses them — this is dynamic programming, not brute force" },
      { wrong: "Deeper networks always learn better with standard backpropagation", correct: "Vanishing gradients make deep networks hard to train — ReLU activations and batch normalization are needed to keep gradients alive" },
      { wrong: "Backpropagation only works for fully connected layers", correct: "It works for any differentiable computation — CNNs, RNNs, transformers, and attention mechanisms all rely on it" },
    ],
    summary: "• Backpropagation efficiently computes gradients of the loss w.r.t. every weight in the network\n• It applies the chain rule layer by layer, propagating error signals from output back to input\n• Intermediate activations are cached during the forward pass and reused — making it as cheap as a second forward pass\n• Vanishing gradients in deep networks are mitigated by ReLU activations, batch normalization, and residual connections\n• It is the algorithmic foundation of all modern deep learning — without it, training deep networks would be infeasible",
  },

  "neural networks": {
    formulas: [
      { formula: "aˡ = σ(Wˡaˡ⁻¹ + bˡ)", meaning: "Each layer applies a linear transformation (weights + bias) followed by a nonlinear activation function" },
      { formula: "ReLU(z) = max(0, z)", meaning: "Rectified linear unit: the most widely used activation — simple, fast, and avoids vanishing gradients" },
      { formula: "σ(z) = 1/(1 + e⁻ᶻ)", meaning: "Sigmoid squashes output to (0, 1) — useful for output probabilities in binary classification" },
      { formula: "L = −Σ yᵢ log(ŷᵢ)", meaning: "Cross-entropy loss for classification — penalizes confident wrong predictions very harshly" },
    ],
    misconceptions: [
      { wrong: "Neural networks work like biological brains", correct: "They are loosely inspired by neurons but are mathematical functions — there is no memory, emotion, or reasoning" },
      { wrong: "More layers always means better performance", correct: "Depth helps up to a point but causes vanishing gradients and overfitting; architecture, data, and regularization matter more" },
      { wrong: "Neural networks understand what they learn", correct: "They learn statistical patterns and correlations in data — not semantic understanding or causal reasoning" },
      { wrong: "You need millions of data points for any neural network to work", correct: "Small networks with strong regularization can generalize well from limited data; transfer learning further reduces data needs" },
    ],
    summary: "• Neural networks are compositions of linear transformations and nonlinear activations, stacked in layers\n• Each layer learns increasingly abstract representations: edges → shapes → objects in vision networks\n• The universal approximation theorem: a sufficiently wide network can approximate any continuous function\n• Training requires a forward pass (prediction), loss computation, backpropagation (gradients), and gradient descent (updates)\n• They power image recognition, language models, drug discovery, and scientific simulation",
  },

  "chain rule": {
    formulas: [
      { formula: "d/dx [f(g(x))] = f′(g(x)) · g′(x)", meaning: "Chain rule: derivative of outer function at the inner, times derivative of the inner — work from outside in" },
      { formula: "dz/dx = dz/dy · dy/dx", meaning: "Leibniz form: derivatives along a chain multiply like fractions — but this is a theorem, not fraction cancellation" },
      { formula: "∂z/∂x = Σᵢ (∂z/∂yᵢ)(∂yᵢ/∂x)", meaning: "Multivariable chain rule: sum over all intermediate paths connecting x to z" },
    ],
    misconceptions: [
      { wrong: "The chain rule only applies to two nested functions", correct: "It applies to any depth of composition — f(g(h(x))) and beyond; just multiply all the local derivatives" },
      { wrong: "You can just multiply derivatives of separate factors", correct: "The product rule handles multiplication; the chain rule handles composition — they are different operations" },
      { wrong: "The chain rule in multiple variables works the same as in one variable", correct: "You must sum over all intermediate paths — each path contributes a product of partial derivatives" },
      { wrong: "dy/dx canceling in the chain rule is just fraction algebra", correct: "The dy notation is not a real fraction; the cancellation appearance is a mnemonic — the chain rule is a deep theorem" },
    ],
    summary: "• The chain rule differentiates composite functions by multiplying derivatives from outside in\n• In Leibniz notation it looks like fraction cancellation — a useful mnemonic, not an algebraic identity\n• The multivariable version sums over all paths connecting variables through intermediate quantities\n• Backpropagation in neural networks is literally the chain rule applied to a computational graph, layer by layer\n• Automatic differentiation (PyTorch, JAX) applies the chain rule systematically at every node — the user never writes derivative code",
  },

  "integrals": {
    formulas: [
      { formula: "∫ₐᵇ f(x) dx = lim(n→∞) Σ f(xᵢ)Δx", meaning: "Definite integral as a limit of Riemann sums — area computed by infinitely thin rectangles" },
      { formula: "∫ xⁿ dx = xⁿ⁺¹/(n+1) + C", meaning: "Power rule for integration — the reverse of the power rule for differentiation" },
      { formula: "∫ₐᵇ f(x) dx = F(b) − F(a)", meaning: "Fundamental Theorem of Calculus: use antiderivatives to evaluate definite integrals — no limit computation needed" },
      { formula: "∫ f(g(x))g′(x) dx = F(g(x)) + C", meaning: "Integration by substitution — the reverse of the chain rule" },
    ],
    misconceptions: [
      { wrong: "The integral is always just the area under the curve", correct: "It measures signed area — regions below the x-axis contribute negatively; you must take absolute value for total area" },
      { wrong: "Integration is just reverse differentiation", correct: "Finding antiderivatives is much harder; many elementary functions have no closed-form antiderivative" },
      { wrong: "The +C doesn't matter in practice", correct: "It encodes the entire family of antiderivatives — omitting it loses information and causes wrong answers in differential equations" },
      { wrong: "Definite and indefinite integrals are the same thing", correct: "Indefinite integral gives a family of functions; definite integral gives a specific number (the accumulated change over an interval)" },
    ],
    summary: "• The definite integral measures accumulated change — signed area between a curve and the x-axis over an interval\n• The Fundamental Theorem of Calculus connects differentiation and integration: antiderivatives make computation practical\n• Riemann sums build geometric intuition; substitution, integration by parts, and partial fractions extend what can be solved\n• Signed area means regions below the axis subtract — total area requires integrating the absolute value\n• Integrals appear in physics (work, flux), probability (expected value), and geometry (arc length, volume)",
  },

  "dot product": {
    formulas: [
      { formula: "a · b = Σ aᵢbᵢ", meaning: "Multiply corresponding components and sum — the algebraic definition, works in any number of dimensions" },
      { formula: "a · b = |a||b|cos(θ)", meaning: "Geometric definition: depends only on the magnitudes and the angle between the vectors" },
      { formula: "a · b = 0 ⟺ a ⊥ b", meaning: "Zero dot product means the vectors are perpendicular — the single fastest orthogonality test" },
      { formula: "proj_b(a) = (a·b / |b|²) b", meaning: "Projection of a onto b: the component of a that lies along b, scaled by b's unit vector" },
    ],
    misconceptions: [
      { wrong: "The dot product gives another vector", correct: "The dot product gives a scalar — a single number, not a vector" },
      { wrong: "Positive dot product just means they're not perpendicular", correct: "Positive dot product means the angle is less than 90° — they point in the same general direction" },
      { wrong: "The dot product formula only works in 2D or 3D", correct: "It works in any dimension — machine learning uses dot products in hundreds or thousands of dimensions" },
      { wrong: "a · b = b · a is obvious from the formula — it doesn't mean anything deep", correct: "Commutativity reflects the geometric fact that the angle between a and b is the same as between b and a" },
    ],
    summary: "• The dot product measures how much two vectors align — it computes a scalar capturing their directional relationship\n• Geometrically: |a||b|cos(θ) — positive means same general direction, zero means perpendicular, negative means opposite\n• Zero dot product is the definition of orthogonality in any number of dimensions\n• Projections, cosine similarity, and orthogonal decomposition all derive directly from the dot product\n• Used in graphics (lighting via surface normals), ML (attention scores, embedding similarity), and physics (work = F · d)",
  },
};

// Normalize topic string for lookup — simple substring matching, no cascading replaces
function normalizeTopic(t) {
  const s = t.toLowerCase().trim();
  if (s.includes("eigen"))              return "eigenvalues and eigenvectors";
  if (s.includes("gradient descent"))   return "gradient descent";
  if (s.includes("linear transform"))   return "linear transformations";
  if (s.includes("backprop"))           return "backpropagation";
  if (s.includes("neural network"))     return "neural networks";
  if (s.includes("chain rule"))         return "chain rule";
  if (s.includes("dot product"))        return "dot product";
  if (s.includes("derivative"))         return "derivatives";
  if (s.includes("determinant"))        return "determinants";
  if (s.includes("integral"))           return "integrals";
  return s;
}

knowledgeRoute.post("/", async (req, res) => {
  const topic = (req.body.topic ?? "").trim();
  const angle = (req.body.angle ?? "").trim();
  if (!topic) return res.status(400).json({ error: "topic is required" });

  // ── Fast path: hardcoded static content ─────────────────────────────────
  const key = normalizeTopic(topic);
  const staticData = STATIC_KNOWLEDGE[key];
  if (staticData && !angle) {
    console.log(`[knowledge] static hit: "${topic}"`);
    return res.json(staticData);
  }

  // ── Slow path: Groq ──────────────────────────────────────────────────────
  const angleCtx = angle ? ` Focus/angle: ${angle}.` : "";
  console.log(`[knowledge] groq call: "${topic}"`);

  try {
    const [formulasResp, misconceptionsResp, summaryResp] = await Promise.all([
      groq.chat.completions.create({
        model: "llama-3.3-70b-versatile",
        messages: [
          {
            role: "system",
            content: `List 4-6 key formulas for the topic. For each: formula (plain text) + one line plain English description of what it means intuitively. Output JSON: { "formulas": [{ "formula": "...", "meaning": "..." }] }`,
          },
          { role: "user", content: `Topic: ${topic}.${angleCtx} JSON only.` },
        ],
        temperature: 0.3,
        max_tokens: 600,
      }),
      groq.chat.completions.create({
        model: "llama-3.3-70b-versatile",
        messages: [
          {
            role: "system",
            content: `List 3-5 common misconceptions. For each: misconception (what students wrongly think) and correct intuition. Output JSON: { "misconceptions": [{ "wrong": "...", "correct": "..." }] }`,
          },
          { role: "user", content: `Topic: ${topic}.${angleCtx} JSON only.` },
        ],
        temperature: 0.4,
        max_tokens: 600,
      }),
      groq.chat.completions.create({
        model: "llama-3.3-70b-versatile",
        messages: [
          {
            role: "system",
            content: `Summarize the topic in 5 bullet points. Each bullet is one important takeaway. Be concise.`,
          },
          { role: "user", content: `Topic: ${topic}.${angleCtx}` },
        ],
        temperature: 0.5,
        max_tokens: 300,
      }),
    ]);

    const parseJson = (text) => {
      let t = text.trim().replace(/^```json\s*/i, "").replace(/```\s*$/i, "").trim();
      try { return JSON.parse(t); } catch { return { formulas: [], misconceptions: [] }; }
    };

    const formulasData      = parseJson(formulasResp.choices[0].message.content);
    const misconceptionsData = parseJson(misconceptionsResp.choices[0].message.content);
    const summary           = summaryResp.choices[0].message.content.trim();

    const formulas      = Array.isArray(formulasData.formulas) ? formulasData.formulas : [];
    const misconceptions = Array.isArray(misconceptionsData.misconceptions) ? misconceptionsData.misconceptions : [];

    return res.json({
      formulas:       formulas.slice(0, 6),
      misconceptions: misconceptions.slice(0, 5),
      summary,
    });
  } catch (err) {
    console.error("[knowledge]", err.message);
    return res.status(500).json({ error: "Failed to generate knowledge", detail: err.message });
  }
});
