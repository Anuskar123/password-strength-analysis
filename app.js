// Password Strength Analysis - JavaScript Implementation

// Constants
const SPECIALS = "!@#$%^&*";
const KEYBOARD_ROWS = ["1234567890", "qwertyuiop", "asdfghjkl", "zxcvbnm"];
const COMMON_SUBSTRINGS = ["password", "admin", "welcome", "qwerty", "letmein"];
const LEET_MAP = { "@": "a", 4: "a", 0: "o", 1: "l", $: "s", 3: "e" };

// Entropy Calculation
function calculateEntropy(password) {
  if (!password) return 0.0;

  let charset = 0;
  if (/[a-z]/.test(password)) charset += 26;
  if (/[A-Z]/.test(password)) charset += 26;
  if (/[0-9]/.test(password)) charset += 10;
  if (
    new RegExp(`[${SPECIALS.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}]`).test(
      password
    )
  ) {
    charset += SPECIALS.length;
  }

  if (charset === 0) return 0.0;
  return Math.round(password.length * Math.log2(charset) * 100) / 100;
}

// Classify Entropy
function classifyEntropy(entropy) {
  const score = Math.min(100, Math.floor(entropy));
  let strength;

  if (score < 40) strength = "Weak";
  else if (score < 65) strength = "Moderate";
  else if (score < 80) strength = "Strong";
  else strength = "Robust";

  return { entropy_bits: entropy, score, strength };
}

// Crack Time Estimate
function crackTimeEstimate(entropy, guessesPerSecond = 1e10) {
  if (entropy <= 0) return { seconds: 0, human: "instant" };

  const seconds = Math.floor(Math.pow(2, entropy) / guessesPerSecond);
  if (seconds < 1) return { seconds, human: "<1s" };

  let value = seconds;
  const parts = [];
  const units = [
    [60, "s"],
    [60, "m"],
    [24, "h"],
    [365, "d"],
  ];
  const labels = ["s", "m", "h", "d", "y"];

  for (let i = 0; i < units.length && value > 0; i++) {
    const [base, label] = units[i];
    parts.push(`${value % base}${labels[i]}`);
    value = Math.floor(value / base);
  }

  if (value > 0) parts.push(`${value}y`);

  return { seconds, human: parts.reverse().join(" ") };
}

// Normalize Leet Speak
function normalizeLeet(str) {
  return str
    .toLowerCase()
    .split("")
    .map((c) => LEET_MAP[c] || c)
    .join("");
}

// Find Patterns
function findPatterns(password) {
  const findings = [];
  const lower = password.toLowerCase();

  // Repeated characters (3+)
  if (/(.)\1{2,}/.test(password)) {
    findings.push("Repeated character run (>=3).");
  }

  // Sequential characters
  for (let i = 0; i < lower.length - 3; i++) {
    const slice = lower.substring(i, i + 4);
    if (/^[a-z0-9]{4}$/.test(slice)) {
      const codes = slice.split("").map((c) => c.charCodeAt(0));
      if (
        codes[1] - codes[0] === 1 &&
        codes[2] - codes[1] === 1 &&
        codes[3] - codes[2] === 1
      ) {
        findings.push(`Ascending sequence '${slice}'.`);
        break;
      }
    }
  }

  // Keyboard walks
  for (const row of KEYBOARD_ROWS) {
    for (let i = 0; i < row.length - 3; i++) {
      const seq = row.substring(i, i + 4);
      if (lower.includes(seq)) {
        findings.push(`Keyboard walk '${seq}'.`);
        break;
      }
    }
  }

  // Common terms
  const normalized = normalizeLeet(lower);
  for (const word of COMMON_SUBSTRINGS) {
    if (lower.includes(word) || normalized.includes(word)) {
      findings.push(`Common term '${word}'.`);
    }
  }

  return findings;
}

// Tokenize Context
function tokenizeContext(contextStr) {
  if (!contextStr) return [];
  return contextStr
    .toLowerCase()
    .split(/[\s,;]+/)
    .filter((t) => t.length >= 3);
}

// Detect Personal Leaks
function detectPersonalLeak(password, tokens) {
  const leaks = [];
  const lower = password.toLowerCase();

  // Check provided tokens
  for (const token of tokens) {
    if (lower.includes(token)) {
      leaks.push(token);
    }
  }

  // Check for years (19xx, 20xx)
  const yearMatches = password.match(/(?:19|20)\d{2}/g);
  if (yearMatches) {
    leaks.push(...yearMatches);
  }

  return [...new Set(leaks)];
}

// Improvement Hints
function improvementHints(password) {
  const hints = [];

  if (password.length < 12) {
    hints.push("Consider length >= 12 for baseline resilience.");
  }
  if (/^[a-zA-Z]+$/.test(password)) {
    hints.push("Add digits and symbols for diversity.");
  }
  if (/^\d+$/.test(password)) {
    hints.push("Add letters and symbols; pure numbers are weak.");
  }
  if (/^[a-z]+$/.test(password)) {
    hints.push("Mix uppercase to raise combinations.");
  }
  if (
    !new RegExp(`[${SPECIALS.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}]`).test(
      password
    )
  ) {
    hints.push(`Introduce specials like ${SPECIALS}.`);
  }

  return hints;
}

// Generate Password
function generatePassword(length = 16) {
  const minLength = 14;
  length = Math.max(length, minLength);

  const pools = {
    lower: "abcdefghijklmnopqrstuvwxyz",
    upper: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    digit: "0123456789",
    special: SPECIALS,
  };

  // Ensure at least one from each pool
  const password = [];
  for (const pool of Object.values(pools)) {
    password.push(pool[Math.floor(Math.random() * pool.length)]);
  }

  // Fill remaining with random characters
  const allChars = Object.values(pools).join("");
  while (password.length < length) {
    password.push(allChars[Math.floor(Math.random() * allChars.length)]);
  }

  // Shuffle
  for (let i = password.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [password[i], password[j]] = [password[j], password[i]];
  }

  return password.join("");
}

// UI Functions
function showTab(tabName) {
  // Hide all tabs
  document.querySelectorAll(".tab-content").forEach((tab) => {
    tab.classList.remove("active");
  });
  document.querySelectorAll(".tab-button").forEach((btn) => {
    btn.classList.remove("active");
  });

  // Show selected tab
  document.getElementById(tabName).classList.add("active");
  event.target.classList.add("active");
}

function togglePasswordVisibility(fieldId) {
  const field = document.getElementById(fieldId);
  const btn = event.target;

  if (field.type === "password") {
    field.type = "text";
    btn.textContent = "︶";
  } else {
    field.type = "password";
    btn.textContent = "👁️";
  }
}

function copyToClipboard(elementId) {
  const element = document.getElementById(elementId);
  const text = element.textContent;

  navigator.clipboard.writeText(text).then(() => {
    const btn = event.target;
    const originalText = btn.textContent;
    btn.textContent = "Copied!";
    btn.classList.add("success");

    setTimeout(() => {
      btn.textContent = originalText;
      btn.classList.remove("success");
    }, 2000);
  });
}

// Analyze Form Handler
document.getElementById("analyzeForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const password = document.getElementById("password").value;
  const contextStr = document.getElementById("context").value;
  const tokens = tokenizeContext(contextStr);

  // Calculate metrics
  const entropy = calculateEntropy(password);
  const result = classifyEntropy(entropy);
  const crackTime = crackTimeEstimate(entropy);
  const patterns = findPatterns(password);
  const leaks = detectPersonalLeak(password, tokens);
  const hints = improvementHints(password);

  // Display results
  const resultsDiv = document.getElementById("analysisResults");
  resultsDiv.classList.remove("hidden");

  // Strength meter
  const strengthBar = document.getElementById("strengthBar");
  strengthBar.style.width = result.score + "%";
  strengthBar.className = "strength-bar " + result.strength.toLowerCase();

  // Basic metrics
  document.getElementById(
    "strengthText"
  ).textContent = `${result.strength} (${result.score}/100)`;
  document.getElementById(
    "entropyText"
  ).textContent = `${result.entropy_bits} bits`;
  document.getElementById("scoreText").textContent = result.score;
  document.getElementById("crackTimeText").textContent = crackTime.human;

  // Patterns
  const patternsSection = document.getElementById("patternsSection");
  if (patterns.length > 0) {
    patternsSection.classList.remove("hidden");
    const patternsList = document.getElementById("patternsList");
    patternsList.innerHTML = patterns.map((p) => `<li>${p}</li>`).join("");
  } else {
    patternsSection.classList.add("hidden");
  }

  // Leaks
  const leaksSection = document.getElementById("leaksSection");
  if (leaks.length > 0) {
    leaksSection.classList.remove("hidden");
    const leaksList = document.getElementById("leaksList");
    leaksList.innerHTML = leaks.map((l) => `<li>${l}</li>`).join("");
  } else {
    leaksSection.classList.add("hidden");
  }

  // Hints
  const hintsSection = document.getElementById("hintsSection");
  if (hints.length > 0) {
    hintsSection.classList.remove("hidden");
    const hintsList = document.getElementById("hintsList");
    hintsList.innerHTML = hints.map((h) => `<li>${h}</li>`).join("");
  } else {
    hintsSection.classList.add("hidden");
  }

  // Suggestion
  const suggestionSection = document.getElementById("suggestionSection");
  if (result.strength === "Weak" || result.strength === "Moderate") {
    suggestionSection.classList.remove("hidden");
    document.getElementById("suggestedPassword").textContent = generatePassword(
      password.length + 2
    );
  } else {
    suggestionSection.classList.add("hidden");
  }

  // Scroll to results
  resultsDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
});

// Generate Form Handler
document
  .getElementById("generateForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const length = parseInt(document.getElementById("length").value);
    const password = generatePassword(length);

    // Display generated password
    const resultsDiv = document.getElementById("generatedPassword");
    resultsDiv.classList.remove("hidden");
    document.getElementById("generatedText").textContent = password;

    // Quick analysis
    const entropy = calculateEntropy(password);
    const result = classifyEntropy(entropy);
    document.getElementById(
      "genEntropy"
    ).textContent = `${result.entropy_bits} bits`;
    document.getElementById("genStrength").textContent = result.strength;
    document.getElementById("genStrength").className =
      result.strength.toLowerCase();

    resultsDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });

// Sync length slider with input
document.getElementById("length").addEventListener("input", function () {
  document.getElementById("lengthSlider").value = this.value;
});

// Batch Scan Function
function scanBatch() {
  const passwordList = document.getElementById("passwordList").value;
  const passwords = passwordList.split("\n").filter((p) => p.trim().length > 0);

  if (passwords.length === 0) {
    alert("Please enter at least one password to scan.");
    return;
  }

  const results = passwords.map((password, index) => {
    const entropy = calculateEntropy(password);
    const result = classifyEntropy(entropy);
    const patterns = findPatterns(password);
    const leaks = detectPersonalLeak(password, []);

    return {
      index: index + 1,
      password: password,
      entropy: result.entropy_bits,
      strength: result.strength,
      issues: [...patterns, ...leaks.map((l) => `Leak: ${l}`)],
    };
  });

  // Calculate stats
  const stats = {
    total: results.length,
    weak: results.filter((r) => r.strength === "Weak").length,
    moderate: results.filter((r) => r.strength === "Moderate").length,
    strong: results.filter((r) => r.strength === "Strong").length,
    robust: results.filter((r) => r.strength === "Robust").length,
  };

  // Display stats
  document.getElementById("totalCount").textContent = stats.total;
  document.getElementById("weakCount").textContent = stats.weak;
  document.getElementById("moderateCount").textContent = stats.moderate;
  document.getElementById("strongCount").textContent = stats.strong;
  document.getElementById("robustCount").textContent = stats.robust;

  // Display table
  const tbody = document.getElementById("batchTableBody");
  tbody.innerHTML = results
    .map(
      (r) => `
        <tr class="${r.strength.toLowerCase()}">
            <td>${r.index}</td>
            <td><code>${
              r.password.length > 20
                ? r.password.substring(0, 20) + "..."
                : r.password
            }</code></td>
            <td><span class="badge ${r.strength.toLowerCase()}">${
        r.strength
      }</span></td>
            <td>${r.entropy} bits</td>
            <td>${
              r.issues.length > 0
                ? r.issues.slice(0, 2).join(", ") +
                  (r.issues.length > 2 ? "..." : "")
                : "None"
            }</td>
        </tr>
    `
    )
    .join("");

  // Show results
  document.getElementById("batchResults").classList.remove("hidden");
  document
    .getElementById("batchResults")
    .scrollIntoView({ behavior: "smooth", block: "nearest" });
}
