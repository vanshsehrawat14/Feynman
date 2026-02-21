/**
 * regen_narration.mjs — Standalone narration regenerator
 * NO GROQ. Scripts are hardcoded. Audio via ElevenLabs directly.
 * Run: node regen_narration.mjs [scene1 scene2 ...]
 */

import "dotenv/config";
import path       from "path";
import { fileURLToPath } from "url";
import { access, unlink, writeFile, readFile, mkdir } from "fs/promises";
import { exec }   from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

process.on("unhandledRejection", (reason) => {
  console.error("\n[FATAL] Unhandled Rejection:", reason?.stack || reason);
  process.exit(1);
});
process.on("uncaughtException", (err) => {
  console.error("\n[FATAL] Uncaught Exception:", err.stack || err);
  process.exit(1);
});

const __dirname    = path.dirname(fileURLToPath(import.meta.url));
const MANIM_DIR    = path.resolve(__dirname, "../manim");
const NARR_DIR     = path.join(MANIM_DIR, "output", "narrated");
const FFMPEG_PATH  = "C:\\ffmpeg\\bin\\ffmpeg.exe";
const FFPROBE_PATH = "C:\\ffmpeg\\bin\\ffprobe.exe";
const ELEVEN_VOICE = "auq43ws1oslv0tO4BDa7";
const ELEVEN_MODEL = "eleven_turbo_v2_5";
const MAX_CHARS    = 2400;  // ElevenLabs safe per-request limit

// ── Scene map ─────────────────────────────────────────────────────────────
const SCENES = {
  eigen:            { video: "la_16_eigen/480p15/EigenScene.mp4",                    topic: "Eigenvalues and Eigenvectors" },
  derivative:       { video: "derivative/480p15/DerivativeScene.mp4",                topic: "Derivatives" },
  gradient_descent: { video: "ml_02_gradient_descent/480p15/GradientDescentScene.mp4", topic: "Gradient Descent" },
  backpropagation:  { video: "ml_03_backpropagation/480p15/BackpropagationScene.mp4",  topic: "Backpropagation" },
  neural_networks:  { video: "ml_01_neural_networks/480p15/NeuralNetworksScene.mp4",   topic: "Neural Networks" },
  integral:         { video: "integral/480p15/IntegralScene.mp4",                    topic: "Integrals" },
  limit:            { video: "limit/480p15/LimitScene.mp4",                          topic: "Limits" },
  chain_rule:       { video: "chain_rule/480p15/ChainRuleScene.mp4",                 topic: "Chain Rule" },
  determinant:      { video: "la_11_determinant/480p15/DeterminantScene.mp4",        topic: "Determinants" },
  linear_transform: { video: "la_06_linear_transform/480p15/LinearTransformScene.mp4", topic: "Linear Transformations" },
  what_matrices_do: { video: "la_21_matrices_geom/480p15/MatricesGeomScene.mp4",     topic: "What Matrices Do Geometrically" },
  vectors:          { video: "la_01_vectors/480p15/VectorsScene.mp4",                topic: "Vectors" },
  matrix_mult:      { video: "la_07_matrix_mult/480p15/MatrixMultScene.mp4",         topic: "Matrix Multiplication" },
  quicksort:        { video: "algo_02_quicksort/480p15/QuicksortScene.mp4",          topic: "Quicksort" },
  game_theory:      { video: "econ_05_game_theory/480p15/GameTheoryScene.mp4",       topic: "Game Theory" },
  induction:        { video: "phys_03_induction/480p15/InductionScene.mp4",          topic: "Electromagnetic Induction" },
  maxwell:          { video: "phys_04_maxwell/480p15/MaxwellScene.mp4",              topic: "Maxwell Equations" },
  dot_product:      { video: "la_04_dot_product/480p15/DotProductScene.mp4",         topic: "Dot Product" },
  cross_product:    { video: "la_05_cross_product/480p15/CrossProductScene.mp4",     topic: "Cross Product" },
  svd:              { video: "la_17_svd/480p15/SVDScene.mp4",                        topic: "Singular Value Decomposition" },
  span:             { video: "la_12_span/480p15/SpanScene.mp4",                      topic: "Span" },
  basis:            { video: "la_14_basis/480p15/BasisScene.mp4",                    topic: "Basis Vectors" },
  det_zero:         { video: "la_22_det_zero/480p15/DetZeroScene.mp4",               topic: "Why Zero Determinant Means No Inverse" },
  bubble_sort:      { video: "algo_01_bubble_sort/480p15/BubbleSortScene.mp4",       topic: "Bubble Sort" },
};

// ── Hardcoded narration scripts (~3-4 min each) ───────────────────────────
const SCRIPTS = {

eigen: `Imagine you have a transformation that stretches, rotates, and shears space. Most vectors get knocked around completely — they change direction, they change magnitude, they end up somewhere entirely different. But hidden inside every matrix, there are special vectors. Vectors that the transformation treats gently. Vectors that don't change direction at all. They just stretch or shrink — scaled by a single number. Those vectors are eigenvectors. Those scaling factors are eigenvalues.

Let's build the intuition geometrically. Picture a two-dimensional transformation — a matrix that stretches space horizontally by a factor of three and leaves the vertical direction unchanged. If you take any random vector, it gets distorted — pulled sideways, its direction changes. But vectors along the horizontal axis? They just triple in length. They point in exactly the same direction before and after. And vectors along the vertical? They don't move at all — scaled by one. These are your eigenvectors, and three and one are your eigenvalues.

This is the core idea. An eigenvector v of a matrix A satisfies A times v equals lambda times v. Lambda is just a number — the eigenvalue. The matrix acts on v exactly the same way that lambda does: pure scaling, no rotation.

Now, how do we find eigenvalues? We ask: for what values of lambda does the equation A minus lambda times the identity matrix, applied to v, equal zero for some nonzero v? This system has a nonzero solution only when A minus lambda I is singular — when its determinant is zero. Setting that determinant to zero gives the characteristic polynomial. Solving the polynomial gives the eigenvalues. Then for each eigenvalue, we substitute back and solve to find the eigenvectors.

Consider a concrete example. Take the matrix with rows two, one and one, two. The characteristic polynomial comes out to lambda squared minus four lambda plus three, which factors as lambda minus one times lambda minus three. So the eigenvalues are one and three. For lambda equals one, we get the eigenvector pointing diagonally. For lambda equals three, we get the one pointing the other diagonal. The matrix stretches along one diagonal by three and leaves the other unchanged.

Why does this matter? Because eigenvalues reveal the essential structure of a transformation. Work in the eigenvector basis, and the matrix becomes diagonal — pure scaling along each axis, nothing more. This is diagonalization. And once diagonal, everything becomes easy: computing powers, exponentials, even solving differential equations.

The applications are everywhere. Principal component analysis uses eigenvectors of the covariance matrix to find the directions of maximum variance in data. In quantum mechanics, eigenvalues are the measurable quantities — energy levels and spin states. Google's PageRank algorithm ranks every page on the internet using the eigenvector of a giant matrix. In structural engineering, eigenvalues reveal natural vibration frequencies.

The trace of a matrix — the sum of its diagonal entries — equals the sum of all eigenvalues. The determinant equals their product. These relationships bind the eigenvalues deep into the fabric of the matrix itself.

So next time you look at a transformation, ask yourself: what directions does this matrix leave unchanged? Find those directions, and you've found the hidden skeleton that everything else is built around.`,

derivative: `Imagine you are driving along a road, and at every instant, you could see not just where you are, but exactly how fast you are changing position. That is the derivative. Not your average speed over the whole trip — your instantaneous speed at each single moment. It is the mathematical tool for measuring change, and it sits at the heart of nearly everything in science and engineering.

Let us build the idea from scratch. You have a function — a curve on a graph. At any point on that curve, you can draw a secant line connecting two points. The slope of that secant tells you the average rate of change between those two points. Now here is the key idea: what happens if you bring those two points closer and closer together, until the gap between them shrinks to zero? The secant line becomes the tangent line — touching the curve at exactly one point. Its slope is the derivative.

Mathematically, the derivative of f at x is the limit of f of x plus h, minus f of x, all divided by h, as h approaches zero. That limit — if it exists — captures the instantaneous rate of change at that single point.

Geometrically, you are measuring the slope of the tangent. Wherever the function rises steeply, the derivative is large and positive. Wherever it falls, the derivative is negative. At a peak or valley, where the function momentarily flattens, the derivative is exactly zero. This is why setting the derivative to zero finds maxima and minima — those are the points where the function changes direction.

You do not have to compute that limit from scratch every time. The power rule says: the derivative of x to the n is n times x to the n minus one. So x squared has derivative two x. The derivative of sine is cosine. The derivative of e to the x is itself — the exponential function is its own rate of change, which is why it appears everywhere in growth and decay.

Consider a falling object. Its height as a function of time is negative one half times g times t squared. Take the derivative and you get negative g times t — the velocity, which grows more negative as it accelerates downward. Take the derivative again and you get negative g — the constant acceleration due to gravity. Two derivatives unlock the entire kinematics of free fall.

The derivative transforms optimization from guesswork into certainty. In economics, the marginal cost is the derivative of the total cost function — it tells you exactly how much one more unit will cost. In machine learning, gradient descent follows derivatives to find parameters that minimize loss. In physics, every fundamental law — from Newton's second law to Maxwell's equations — is written in the language of derivatives.

The moment you understand the derivative geometrically — as a tangent slope, as an instantaneous rate of change — the rest of calculus becomes natural. It is the single most powerful idea for understanding how things change.`,

gradient_descent: `Imagine you are standing blindfolded on a hilly landscape, and you want to find the lowest valley. You cannot see the whole terrain, but you can feel the slope under your feet right where you are standing. The obvious strategy: take a step in the direction the ground slopes downward, then repeat. That intuition is gradient descent — the algorithm behind training virtually every neural network in the world.

Let us make this precise. You have a loss function — a surface whose height represents how wrong your model is at any configuration of parameters. The goal is to find the parameters that make this surface as low as possible. At any point on the surface, the gradient is a vector pointing in the direction of steepest ascent — straight uphill. To descend, you move in the opposite direction: the negative gradient.

The update rule is simple: theta new equals theta old minus alpha times the gradient of the loss evaluated at theta old. Alpha is the learning rate — the size of each step. This single equation, applied thousands or millions of times, is how neural networks learn from data.

The learning rate is everything. Too large, and you overshoot valleys — parameters bounce around wildly and the loss might actually increase. Too small, and progress is agonizingly slow — you take baby steps across a vast landscape. Adaptive methods like Adam adjust the learning rate automatically based on the history of gradients, which is why they are so widely used in practice.

For convex functions — bowl-shaped surfaces — gradient descent is guaranteed to find the global minimum. The loss has one unique valley, and every step brings you closer. For the nonconvex surfaces of deep neural networks, there is no such guarantee. But here is what is remarkable: in practice, gradient descent finds solutions that work extraordinarily well. The landscape of deep networks, while complicated, has structure that gradient descent exploits efficiently.

The naive version computes the gradient using all training examples at once. This is expensive. Stochastic gradient descent picks a single random example and computes a noisy approximation. Mini-batch gradient descent — the standard in practice — uses a small subset, balancing noise and efficiency. The noise in stochastic methods actually helps: it shakes the parameters out of shallow local minima.

There are practical extensions: momentum builds up velocity in consistent directions, helping you roll through shallow valleys and speed up convergence. Weight decay penalizes large parameters, keeping things from exploding.

But the core idea remains the hill descent. Feel the slope, step downhill, repeat. The elegance is that you never need to see the whole landscape — only the local gradient at your current position. That local information, accumulated over millions of steps, is enough to sculpt a neural network that recognizes faces, translates languages, or predicts the shape of a protein.`,

linear_transform: `What does a matrix actually do? Every time you multiply a vector by a matrix, something happens to space. Points move. Arrows stretch. Grids deform. And yet, something profound is preserved through all of this. That something is linearity — and it is the foundation of all of linear algebra.

A linear transformation is a function from one vector space to another that preserves two fundamental operations: addition and scalar multiplication. If you add two vectors and transform the result, it is the same as transforming each separately and adding. If you scale a vector and transform it, it is the same as transforming it and then scaling. These two rules — additivity and homogeneity — are the only requirements. And they impose an enormous amount of structure.

Here is the key insight: a linear transformation is completely determined by what it does to the basis vectors. If you know where the standard basis vectors — the unit vectors along each axis — land after the transformation, you know everything. Because any other vector is just a linear combination of basis vectors, and linearity tells you that the transformation of a linear combination is the linear combination of the transformations.

This is why matrices are the right tool. The columns of a matrix are exactly the images of the basis vectors. The first column is where the first basis vector lands. The second column is where the second basis vector lands. Multiplying a vector by the matrix applies the transformation. It is not just a computational trick — it is the geometric operation itself.

Let us see this concretely. A rotation matrix that rotates everything by ninety degrees takes the horizontal vector and sends it to the vertical, and takes the vertical vector and sends it to the negative horizontal. Write those destination vectors as columns, and you have the rotation matrix. No memorization needed — just track where the basis vectors go.

What kinds of transformations are linear? Rotations, reflections, scaling, shearing, projection — all linear. What is not linear? Translation — moving everything in one direction — breaks additivity. That is why computer graphics uses homogeneous coordinates: lifting transformations into a higher dimension so that translations can also be written as matrix multiplications.

The composition of two linear transformations is also linear. And the matrix representing the composition is the product of the two matrices — applied right to left. This is why matrix multiplication is defined the way it is. It is not an arbitrary formula. It is function composition.

Linear transformations are the language in which physics, graphics, machine learning, and data science are written. Every layer of a neural network is a linear transformation followed by a nonlinearity. Every rendering pipeline in computer graphics applies sequences of linear transformations. Every time you rotate, scale, or project — you are composing linear maps.`,

determinant: `When a matrix acts on space, it changes areas and volumes. A transformation might stretch things out, compress them, rotate them, or flip them over. The determinant is the single number that measures exactly how much the transformation scales these areas and volumes — and whether it flips orientation in the process.

Think of the two columns of a two-by-two matrix as two arrows anchored at the origin. Together they define a parallelogram. The determinant is the signed area of that parallelogram. If the columns point in roughly the same direction, the parallelogram is thin — the transformation compresses space. If the columns are nearly perpendicular and long, the area is large — the transformation stretches space. And if the columns are parallel, the parallelogram collapses entirely to a line, and the area is zero.

That zero case is crucial. A determinant of zero means the transformation is singular — it collapses space down by at least one dimension. Vectors that were spread out in two dimensions get squashed onto a line. Once you have lost a dimension, you cannot recover it — the transformation has no inverse.

The sign of the determinant matters too. A positive determinant means the transformation preserves orientation. A negative determinant means orientation is flipped — a reflection has occurred somewhere. In two dimensions, this means the counterclockwise angle from the first column to the second became clockwise.

For a two-by-two matrix with entries a, b, c, d — the determinant is a times d minus b times c. This is the difference between the products of the diagonal and anti-diagonal elements. For larger matrices, you can expand along rows or columns, reduce to triangular form, or use cofactors. In triangular form, the determinant is simply the product of the diagonal entries.

Key properties: the determinant of a product of matrices is the product of their determinants. Swapping two rows flips the sign. Multiplying a row by a constant multiplies the determinant by that constant. Adding a multiple of one row to another leaves the determinant unchanged — this is why row reduction works.

And perhaps most powerfully: eigenvalues are the values that make the determinant of A minus lambda times the identity equal to zero. The characteristic polynomial — the tool for finding all eigenvalues — is fundamentally a determinant calculation.

Learn to read the determinant geometrically. It is not just a formula — it is the measure of how boldly a matrix reshapes the world.`,

backpropagation: `Neural networks learn by adjusting millions of weights, nudging each one in the direction that reduces error on training data. But how do you know which direction to nudge each weight? How do you compute the derivative of the final loss with respect to a weight buried deep in an early layer of the network? That is what backpropagation solves — and it solves it elegantly.

The forward pass is straightforward: you feed input data through the network, layer by layer, computing activations and finally a prediction. You compare that prediction to the ground truth and compute the loss — a number measuring how wrong the network is. Now you need gradients: how does the loss change if you increase each weight by a tiny amount?

The naive approach would be to perturb each weight one at a time and measure the change in loss. For a network with millions of weights, this is computationally catastrophic. Backpropagation does it in a single backward pass, by exploiting the chain rule of calculus.

The chain rule says: if y depends on z, which depends on x, then the rate at which y changes with respect to x equals the rate y changes with respect to z, times the rate z changes with respect to x. In a neural network, this chain extends through all the layers, from output back to input. Backpropagation computes these derivatives systematically, starting at the output and working backward. At each layer, it takes the error signal from the layer ahead, multiplies by the local derivative, and passes the result further back.

Crucially, intermediate computations from the forward pass are cached and reused — this is dynamic programming. The cost of computing all gradients is approximately the same as a second forward pass. Without this caching, the computation would be exponentially more expensive.

The resulting gradients drive gradient descent: each weight moves opposite to its gradient, scaled by the learning rate. Repeat this process over millions of training examples, and the network gradually learns the structure of the data.

There are subtleties. In deep networks, the repeated multiplication of gradients through many layers can make them vanish — shrink to nearly zero before they reach early layers. This is the vanishing gradient problem. It plagued deep learning for years until ReLU activations and batch normalization were introduced, keeping gradients alive through many layers.

Modern frameworks like PyTorch and JAX build a computational graph dynamically during the forward pass, then traverse it in reverse to compute exact gradients automatically. The user never writes derivative code. Backpropagation is quiet, invisible, and running in the background of every image recognized, every sentence translated, every drug discovered by a neural network.`,

neural_networks: `There is a class of mathematical functions that can, in principle, approximate anything. Feed them enough data and the right training procedure, and they learn to recognize faces, translate languages, predict molecular structures, and generate coherent text. These are neural networks — and despite their name, they have less to do with biology than with elegant mathematics.

The building block is simple: take a vector of inputs, multiply each by a learnable weight, sum them up, add a bias, and apply a nonlinear function. That is one artificial neuron. Stack hundreds or thousands of these in a layer, then stack many such layers, and you have a deep neural network. Each layer transforms its input according to the formula: activation equals sigma of W times a plus b, where W is the weight matrix, a is the input, b is the bias, and sigma is a nonlinear activation function.

The activation function is what gives networks their power. Without it, every layer would be a linear transformation, and composing linear transformations just produces another linear transformation — no depth would help. Apply a nonlinearity after each layer — something as simple as the rectified linear unit, which is just the maximum of zero and the input — and suddenly you can represent functions of arbitrary complexity.

The universal approximation theorem formalizes this: a network with even a single hidden layer and enough neurons can approximate any continuous function to arbitrary precision. In practice, depth matters more than width — deeper networks are far more parameter-efficient. Each layer learns increasingly abstract representations: in an image network, early layers detect edges, middle layers detect shapes, and deep layers recognize objects.

Training a neural network means finding weights that minimize a loss function — a measure of how wrong the predictions are. You start with random weights, make predictions, compute the loss, compute gradients via backpropagation, and update the weights using gradient descent. Repeat this for millions of examples and the network gradually learns the structure of the data.

The architecture of the network — how layers are connected, what operations they perform — matters enormously. Convolutional networks process images by sharing weights across spatial locations. Recurrent networks handle sequences by maintaining hidden state. Transformers process all positions in parallel using attention mechanisms, and have become dominant in language, vision, and scientific discovery.

What neural networks learn is statistical structure: patterns, correlations, regularities in data. They do not reason, plan, or understand in a human sense. But for tasks where large amounts of data encode the relevant structure — perception, prediction, generation — they are extraordinarily effective tools for science and engineering.`,

chain_rule: `Imagine you are at a factory. The temperature of a furnace depends on the fuel flow rate, and the fuel flow rate depends on a control dial you are turning. You want to know: if you turn the dial, how does the furnace temperature change? The answer requires two pieces: how sensitive temperature is to fuel flow, and how sensitive fuel flow is to the dial position. Multiply them together and you have your answer. That is the chain rule.

The chain rule is the rule for differentiating composite functions — functions built by nesting one function inside another. If h of x equals f of g of x, then the derivative of h with respect to x is the derivative of f evaluated at g of x, times the derivative of g with respect to x. In Leibniz notation: dz over dx equals dz over dy times dy over dx. It looks like fractions canceling — and while that is a useful mnemonic, it is a theorem, not fraction algebra.

Let us see it concretely. What is the derivative of the sine of x squared? The outer function is sine. The inner function is x squared. The derivative of sine is cosine, so the outer derivative at the inner is cosine of x squared. The derivative of the inner is two x. Multiply: two x times cosine of x squared.

The chain rule extends to any depth of composition. The derivative of f of g of h of x is the derivative of f at g of h of x, times the derivative of g at h of x, times the derivative of h at x. Each layer contributes a multiplicative factor.

In multiple variables, the chain rule generalizes via partial derivatives. If z depends on several intermediate variables, each of which depends on x, then the total derivative of z with respect to x is the sum over all paths: partial z over partial y i, times partial y i over partial x. You account for every route through which a change in x can propagate to affect z.

This multivariable form is exactly what backpropagation computes in neural networks. The loss is a function of the outputs, which are functions of the layer activations, which are functions of the weights. Backprop traces these dependencies, applying the chain rule at every node in the computational graph. Automatic differentiation — the technology inside PyTorch and TensorFlow — is systematic application of the chain rule at every operation. The user never writes derivative code. The framework derives it automatically from the forward computation.

The chain rule might seem like a mechanical rule, but it encodes something deep: derivatives multiply along chains of dependence. Whenever quantities are connected by function composition, the sensitivity of one to another is the product of all the intermediate sensitivities along the chain. That is a profound and universal truth about how change propagates through complex systems.`,

integral: `The derivative tells you the rate of change. The integral tells you the accumulated change. If the derivative is the speedometer reading at each instant, the integral is the total distance traveled. These two operations — differentiation and integration — are opposite faces of the same coin, bound together by one of the most beautiful theorems in all of mathematics.

The core idea of integration is summation. Suppose you want to find the area under a curve — the region between a function and the horizontal axis over some interval. You could approximate it with rectangles. Divide the interval into narrow strips, draw a rectangle on each strip with height equal to the function value, and add up all the areas. This is a Riemann sum. The approximation improves as the rectangles get narrower. Take the limit as their width shrinks to zero, and you get the exact area — the definite integral.

The definite integral is written with the integral sign, the lower limit below, the upper limit above, then f of x, then d x. That d x is not just notation — it represents the infinitesimally thin width of each rectangle. The integral sign itself is an elongated S for sum: a continuous sum of infinitely many infinitely thin rectangles.

The Fundamental Theorem of Calculus connects this geometric idea to differentiation. If F is any antiderivative of f — meaning F prime equals f — then the definite integral of f from a to b equals F of b minus F of a. Instead of computing a limit of Riemann sums, you find an antiderivative and evaluate it at the endpoints. This is what makes integration computationally tractable.

Finding antiderivatives is harder than differentiation. Not every function has a closed-form antiderivative. Techniques like substitution, integration by parts, and partial fractions extend the range of what you can integrate analytically. Many other integrals require numerical methods.

Signed area is the key geometric interpretation. Regions where f is positive contribute positively. Regions where f is negative contribute negatively. If you want total area regardless of sign, you integrate the absolute value.

Integrals appear everywhere. In physics, the work done by a force along a path is the integral of force over displacement. Electric and gravitational fields are computed by integrating over charge and mass distributions. In probability, the expected value of a continuous random variable is the integral of x times its probability density. In geometry, arc length, surface area, and volume all require integration.

The integral is the mathematical expression of accumulation. Wherever something builds up continuously over time or space — heat, charge, probability, distance — the integral is the natural language for describing it.`,

dot_product: `Two vectors sit in space. They have magnitudes — lengths — and they point in particular directions. The dot product is the operation that captures, in a single number, how much these two vectors align. It is the simplest way to ask: are these vectors pointing in the same direction, or opposite directions, or somewhere in between?

Algebraically, the dot product is computed component by component. Multiply the corresponding components of two vectors, and add up the results. For vectors a and b in three dimensions, it is a one times b one, plus a two times b two, plus a three times b three. The result is a scalar — a single number, not a vector. This is worth emphasizing: the dot product takes two vectors and returns a number. Not another vector. A number.

But the geometric meaning is what makes the dot product profound. The dot product of a and b equals the magnitude of a times the magnitude of b times the cosine of the angle between them. This formula reveals everything about the relationship between the two vectors.

If the dot product is positive, the cosine is positive, which means the angle is less than ninety degrees — the vectors point in the same general direction. If the dot product is zero, the cosine is zero, meaning the angle is exactly ninety degrees — the vectors are perpendicular, or orthogonal. If the dot product is negative, the angle exceeds ninety degrees — the vectors point in generally opposite directions.

This makes orthogonality testable in one calculation. You do not need to measure angles directly. Just compute the dot product: if it is zero, the vectors are perpendicular. This is why inner products and orthogonality are so central to linear algebra and Fourier analysis — they give you a way to decompose signals, project onto subspaces, and find independent directions.

The projection formula follows directly. The projection of vector a onto vector b — the component of a that lies along b — equals a dot b divided by the magnitude of b, times the unit vector in b's direction. The scalar part is the signed length of the shadow that a casts on b.

In machine learning, the dot product is the engine of similarity. Cosine similarity between two vectors is their dot product divided by the product of their magnitudes — the cosine of the angle between them. Attention mechanisms in transformers compute dot products between query and key vectors to determine how much each token should attend to each other token.

In physics, the work done by a force is the dot product of the force vector and the displacement vector. Only the component of force along the direction of motion does work. The dot product selects that component automatically.

The dot product is multiplication for vectors — a way of combining two vectors into a meaningful scalar that knows about geometry. It measures alignment, similarity, projection, and orthogonality all in one operation.`,
};

// ── Split text into chunks ≤ maxChars at sentence boundaries ──────────────
function splitIntoChunks(text, maxChars = MAX_CHARS) {
  const sentences = text.match(/[^.!?]+[.!?]+(\s|$)/g) || [text];
  const chunks = [];
  let current = "";
  for (const sentence of sentences) {
    if ((current + sentence).length > maxChars && current.length > 0) {
      chunks.push(current.trim());
      current = sentence;
    } else {
      current += sentence;
    }
  }
  if (current.trim()) chunks.push(current.trim());
  return chunks;
}

// ── ElevenLabs TTS — direct call, no fallback ────────────────────────────
async function elevenLabsTTS(text) {
  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) throw new Error("ELEVENLABS_API_KEY not set");
  const trimmed = text.trim();
  if (!trimmed) throw new Error("Empty text passed to TTS");

  console.log(`  [TTS] ${trimmed.length} chars → ElevenLabs...`);

  const response = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${ELEVEN_VOICE}`,
    {
      method: "POST",
      headers: {
        "xi-api-key":   apiKey,
        "Content-Type": "application/json",
        Accept:         "audio/mpeg",
      },
      body: JSON.stringify({
        text: trimmed,
        model_id: ELEVEN_MODEL,
        voice_settings: { stability: 0.45, similarity_boost: 0.80 },
      }),
    }
  );

  if (!response.ok) {
    const errText = await response.text().catch(() => "");
    throw new Error(`ElevenLabs ${response.status}: ${errText.slice(0, 300)}`);
  }

  const bytes = Buffer.from(await response.arrayBuffer());
  if (bytes.length < 500) throw new Error(`ElevenLabs returned tiny audio (${bytes.length} bytes)`);
  console.log(`  [TTS] OK — ${bytes.length} bytes`);
  return bytes;
}

// ── ffprobe: get media duration ───────────────────────────────────────────
async function getMediaDuration(filePath) {
  const pyScript = [
    "import subprocess",
    `path = r'${filePath.replace(/\\/g, "\\\\")}'`,
    `ffprobe = r'${FFPROBE_PATH.replace(/\\/g, "\\\\")}'`,
    "r = subprocess.run([ffprobe, '-v', 'error', '-show_entries', 'format=duration',",
    "  '-of', 'default=noprint_wrappers=1:nokey=1', path],",
    "  capture_output=True, text=True, timeout=30)",
    "print(r.stdout.strip() or '0')",
  ].join("\n");
  const tmpPy = path.join(NARR_DIR, "_probe_dur.py");
  try {
    await writeFile(tmpPy, pyScript, "utf8");
    const { stdout } = await execAsync(`python "${tmpPy}"`, { timeout: 30_000 });
    return parseFloat(stdout.trim()) || 0;
  } catch (err) {
    console.warn(`  [probe] duration error: ${err.message}`);
    return 0;
  }
}

// ── ffmpeg: concatenate MP3s ──────────────────────────────────────────────
async function concatMP3s(paths, outputPath) {
  const concatLines = paths.map(p => `file '${p.replace(/\\/g, "/")}'`);
  const concatFile  = outputPath.replace(/\.mp3$/, "_concatlist.txt");
  await writeFile(concatFile, concatLines.join("\n"), "utf8");

  const pyScript = [
    "import subprocess, sys",
    `ffmpeg = r'${FFMPEG_PATH.replace(/\\/g, "\\\\")}'`,
    `concat_file = r'${concatFile.replace(/\\/g, "\\\\")}'`,
    `output = r'${outputPath.replace(/\\/g, "\\\\")}'`,
    "cmd = [ffmpeg, '-y', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', output]",
    "r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)",
    "print('rc:', r.returncode)",
    "if r.returncode != 0: print('err:', r.stderr[-400:]); sys.exit(1)",
    "print('size:', __import__('os').path.getsize(output))",
  ].join("\n");

  const tmpPy = path.join(NARR_DIR, "_concat_tmp.py");
  await writeFile(tmpPy, pyScript, "utf8");
  const { stdout, stderr } = await execAsync(`python "${tmpPy}"`, { timeout: 180_000 });
  if (stdout) console.log(`  [concat] ${stdout.trim()}`);
  if (stderr) console.warn(`  [concat stderr] ${stderr.trim().slice(0, 200)}`);
}

// ── ffmpeg: sync-aware merge ──────────────────────────────────────────────
async function mergeAudioVideo(videoPath, audioPath, outputPath) {
  let audioDur, videoDur;
  try {
    audioDur = await getMediaDuration(audioPath);
    videoDur = await getMediaDuration(videoPath);
  } catch (err) {
    throw new Error(`Duration probe failed: ${err.message}`);
  }

  const diff = audioDur - videoDur;
  console.log(`  [merge] video: ${videoDur.toFixed(1)}s  audio: ${audioDur.toFixed(1)}s  diff: ${diff.toFixed(1)}s`);

  let pyScript;

  if (diff > 5) {
    const ratio = (audioDur / videoDur).toFixed(6);
    console.log(`  [merge] audio longer — slowing video (ratio ${ratio})`);
    pyScript = [
      "import subprocess, sys, os",
      `ffmpeg = r'${FFMPEG_PATH.replace(/\\/g, "\\\\")}'`,
      `video  = r'${videoPath.replace(/\\/g, "\\\\")}'`,
      `audio  = r'${audioPath.replace(/\\/g, "\\\\")}'`,
      `output = r'${outputPath.replace(/\\/g, "\\\\")}'`,
      `ratio  = ${ratio}`,
      "cmd = [ffmpeg, '-y', '-i', video, '-i', audio,",
      "       '-filter:v', f'setpts={ratio}*PTS', '-c:a', 'aac', '-shortest', output]",
      "r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)",
      "print('rc:', r.returncode)",
      "if r.returncode != 0: print('err:', r.stderr[-600:]); sys.exit(1)",
      "print('size:', os.path.getsize(output))",
    ].join("\n");

  } else if (diff < -5) {
    const paddedPath = audioPath.replace(/\.mp3$/, "_padded.mp3");
    console.log(`  [merge] video longer — padding audio`);
    pyScript = [
      "import subprocess, sys, os",
      `ffmpeg     = r'${FFMPEG_PATH.replace(/\\/g, "\\\\")}'`,
      `video      = r'${videoPath.replace(/\\/g, "\\\\")}'`,
      `audio      = r'${audioPath.replace(/\\/g, "\\\\")}'`,
      `padded     = r'${paddedPath.replace(/\\/g, "\\\\")}'`,
      `output     = r'${outputPath.replace(/\\/g, "\\\\")}'`,
      `video_dur  = ${videoDur.toFixed(3)}`,
      "r1 = subprocess.run([ffmpeg, '-y', '-i', audio, '-af', f'apad=whole_dur={video_dur}', padded],",
      "  capture_output=True, text=True, timeout=120)",
      "if r1.returncode != 0: print('pad err:', r1.stderr[-300:]); sys.exit(1)",
      "r2 = subprocess.run([ffmpeg, '-y', '-i', video, '-i', padded,",
      "  '-c:v', 'copy', '-c:a', 'aac', '-shortest', output],",
      "  capture_output=True, text=True, timeout=600)",
      "print('rc:', r2.returncode)",
      "if r2.returncode != 0: print('err:', r2.stderr[-600:]); sys.exit(1)",
      "print('size:', os.path.getsize(output))",
      "try: os.unlink(padded)",
      "except: pass",
    ].join("\n");

  } else {
    console.log(`  [merge] durations close — direct merge`);
    pyScript = [
      "import subprocess, sys, os",
      `ffmpeg = r'${FFMPEG_PATH.replace(/\\/g, "\\\\")}'`,
      `video  = r'${videoPath.replace(/\\/g, "\\\\")}'`,
      `audio  = r'${audioPath.replace(/\\/g, "\\\\")}'`,
      `output = r'${outputPath.replace(/\\/g, "\\\\")}'`,
      "cmd = [ffmpeg, '-y', '-i', video, '-i', audio, '-c:v', 'copy', '-c:a', 'aac', '-shortest', output]",
      "r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)",
      "print('rc:', r.returncode)",
      "if r.returncode != 0: print('err:', r.stderr[-600:]); sys.exit(1)",
      "print('size:', os.path.getsize(output))",
    ].join("\n");
  }

  const tmpPy = path.join(NARR_DIR, "_merge_tmp.py");
  await writeFile(tmpPy, pyScript, "utf8");
  const { stdout, stderr } = await execAsync(`python "${tmpPy}"`, { timeout: 600_000 });
  if (stdout) console.log(`  [merge] ${stdout.trim()}`);
  if (stderr) console.warn(`  [merge stderr] ${stderr.trim().slice(0, 300)}`);

  return { audioDur, videoDur };
}

// ── Delete old output files for a base name ───────────────────────────────
async function deleteExisting(baseName) {
  const files = [
    path.join(NARR_DIR, `${baseName}_narrated.mp4`),
    path.join(NARR_DIR, `${baseName}_audio.mp3`),
    path.join(NARR_DIR, `${baseName}_audio_concatlist.txt`),
  ];
  for (let i = 1; i <= 10; i++) files.push(path.join(NARR_DIR, `${baseName}_chunk${i}.mp3`));
  for (const p of files) {
    try { await unlink(p); console.log(`  Deleted: ${path.basename(p)}`); }
    catch { /* not found */ }
  }
}

// ── Process one scene using hardcoded script ──────────────────────────────
async function processScene(name) {
  console.log(`\n${"=".repeat(60)}`);
  console.log(`Scene: ${name}`);

  const scene = SCENES[name];
  if (!scene) {
    console.error(`Unknown scene "${name}". Available: ${Object.keys(SCENES).join(", ")}`);
    return false;
  }

  const script = SCRIPTS[name];
  if (!script) {
    console.error(`No hardcoded script for "${name}". Add it to SCRIPTS first.`);
    return false;
  }

  const videoAbsPath = path.join(MANIM_DIR, "output", "videos", ...scene.video.split("/"));
  const baseName     = path.basename(videoAbsPath, ".mp4");

  console.log(`Topic:  ${scene.topic}`);
  console.log(`Video:  ${videoAbsPath}`);
  console.log(`Script: ${script.trim().split(/\s+/).length} words`);

  try {
    await access(videoAbsPath);
    console.log(`Video:  exists OK`);
  } catch (err) {
    console.error(`Video NOT found: ${videoAbsPath}`);
    console.error(`access error: ${err.message}`);
    return false;
  }

  await mkdir(NARR_DIR, { recursive: true });
  await deleteExisting(baseName);

  const audioPath  = path.join(NARR_DIR, `${baseName}_audio.mp3`);
  const narrPath   = path.join(NARR_DIR, `${baseName}_narrated.mp4`);
  const start      = Date.now();

  try {
    // 1. Split script into chunks ≤ 2400 chars
    const chunks = splitIntoChunks(script.trim());
    console.log(`\n  Script split into ${chunks.length} chunk(s)`);

    // 2. TTS each chunk
    const chunkPaths = [];
    for (let i = 0; i < chunks.length; i++) {
      const audioBytes = await elevenLabsTTS(chunks[i]);
      const chunkPath  = path.join(NARR_DIR, `${baseName}_chunk${i + 1}.mp3`);
      await writeFile(chunkPath, audioBytes);
      chunkPaths.push(chunkPath);
    }

    // 3. Concatenate chunks into one audio file
    console.log(`\n  Concatenating ${chunkPaths.length} chunk(s)...`);
    if (chunkPaths.length === 1) {
      const buf = await readFile(chunkPaths[0]);
      await writeFile(audioPath, buf);
    } else {
      await concatMP3s(chunkPaths, audioPath);
    }

    // 4. Sync-aware merge with video
    console.log(`\n  Merging audio with video...`);
    const { audioDur, videoDur } = await mergeAudioVideo(videoAbsPath, audioPath, narrPath);

    // 5. Verify output
    let outputSize = 0;
    try {
      const { stdout } = await execAsync(`python -c "import os; print(os.path.getsize(r'${narrPath.replace(/\\/g, "\\\\")}'))"`);
      outputSize = parseInt(stdout.trim()) || 0;
    } catch { /* ignore */ }

    // 6. Cleanup chunks
    for (const p of chunkPaths) {
      try { await unlink(p); } catch { /* ignore */ }
    }

    const elapsed = ((Date.now() - start) / 1000).toFixed(1);
    console.log(`\n  SUCCESS (${elapsed}s)`);
    console.log(`  Output:   ${narrPath}`);
    console.log(`  Size:     ${(outputSize / 1024 / 1024).toFixed(2)} MB`);
    console.log(`  Audio:    ${audioDur.toFixed(1)}s`);
    console.log(`  Video:    ${videoDur.toFixed(1)}s`);
    return true;

  } catch (err) {
    console.error(`\n  FAILED: ${err.message}`);
    console.error(`  Stack:\n${err.stack}`);
    return false;
  }
}

// ── Main ──────────────────────────────────────────────────────────────────
const args      = process.argv.slice(2);
const toProcess = args.length > 0 ? args : ["eigen"];

console.log(`\nFeynman Narration Regenerator (NO-GROQ MODE)`);
console.log(`Voice: ${ELEVEN_VOICE} (Adam) | Model: ${ELEVEN_MODEL}`);
console.log(`Scenes: ${toProcess.join(", ")}`);

if (!process.env.ELEVENLABS_API_KEY) {
  console.error("\nFATAL: ELEVENLABS_API_KEY not set");
  process.exit(1);
}
console.log(`ElevenLabs key: set (length=${process.env.ELEVENLABS_API_KEY.length})`);
console.log(`NARR_DIR: ${NARR_DIR}`);

for (const name of toProcess) {
  let ok = false;
  try {
    ok = await processScene(name);
  } catch (err) {
    console.error(`\n[main] processScene("${name}") threw:`);
    console.error(err.stack || err.message);
    ok = false;
  }

  if (!ok) {
    console.error(`\nStopping on failure of "${name}".`);
    process.exit(1);
  }
}

console.log(`\nAll done.`);
