import { use, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Home, ArrowRight, Moon, Sun, Search } from "lucide-react";

export default function SearchPage() {
  const navigate = useNavigate();
  const [darkMode, setDarkMode] = useState(false);

  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [requiredConcepts, setRequiredConcepts] = useState([]);
  const [supportingConcepts, setSupportingConcepts] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!query.trim()) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
        }),
      });

      if (!response.ok) {
        throw new Error("Search request failed.");
      }

      const data = await response.json();

      setRequiredConcepts(data.required_concepts || []);

      setSupportingConcepts(data.supporting_concepts || []);

      setResults(data.results || []);
    } catch (err) {
      console.error(err);

      setError("Could not connect to the search server.");

      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`
  min-h-screen
  transition-colors duration-300
  ${
    darkMode
      ? `
        bg-black
        [background-image:linear-gradient(to_right,_rgba(255,_255,_255,_0.18)_1px,_transparent_1px),_linear-gradient(to_bottom,_rgba(255,_255,_255,_0.18)_1px,_transparent_1px)]
      `
      : `
        bg-white
        [background-image:linear-gradient(to_right,_rgba(148,_163,_184,_0.55)_1px,_transparent_1px),_linear-gradient(to_bottom,_rgba(148,_163,_184,_0.55)_1px,_transparent_1px)]
      `
  }
  [background-size:35px_35px]
`}
    >
      {/* Navbar */}
      <nav className="flex items-center justify-between px-10 py-6">
        {/* Logo */}
        <div
          className={`text-xl font-bold ${
            darkMode ? "text-white" : "text-slate-900"
          }`}
        >
          LeetCodeFind
        </div>

        {/* Right side */}
        <div className="flex items-center gap-3">
          {/* Home */}
          <button
            onClick={() => navigate("/")}
            className={`group flex items-center gap-1.5 transition-colors duration-200 ${
              darkMode
                ? "text-white hover:text-white"
                : "text-slate-600 hover:text-black"
            }`}
          >
            <Home size={18} className="transition-colors duration-200" />
            <span>Home</span>
          </button>

          {/* Brightness toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`rounded-full p-2 transition-colors duration-200 ${
              darkMode
                ? "text-white hover:bg-white/10"
                : "text-gray-700 hover:bg-black/5"
            }`}
          >
            {darkMode ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>
      </nav>

      {/* Main Search Section */}
      <main className="flex min-h-[calc(100vh-100px)] items-center justify-center px-6">
        <div className="w-full max-w-3xl text-center">
          {/* Heading */}
          <div className="mb-10">
            <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-[#FFA116]">
              Intelligent Problem Search
            </p>

            <h1
              className={`text-5xl font-bold tracking-tight ${
                darkMode ? "text-white" : "text-slate-900"
              }`}
            >
              Find the right
              <span className="text-[#FFA116]">
                {" "}
                LeetCode problem for yourself
              </span>
            </h1>

            <p
              className={`mx-auto mt-5 max-w-xl text-lg leading-8 ${
                darkMode ? "text-slate-300" : "text-slate-600"
              }`}
            >
              Describe the problem you're trying to solve and discover relevant
              LeetCode questions using semantic search.
            </p>
          </div>

          {/* Search Box */}
          <div className="mx-auto max-w-2xl">
            <div
              className={`
    flex items-center
    rounded-2xl
    border
    p-2
    shadow-xl
    transition-all
    duration-300
    ${
      darkMode
        ? `
          border-slate-700
          bg-[#111111]
          shadow-black/40
          focus-within:border-[#FFA116]
          focus-within:ring-4
          focus-within:ring-[#FFA116]/10
        `
        : `
          border-slate-300
          bg-white
          shadow-slate-200/50
          focus-within:border-blue-500
          focus-within:ring-4
          focus-within:ring-blue-100
        `
    }
  `}
            >
              <Search className="ml-4 h-5 w-5 text-slate-400" />

              <input
                type="text"
                placeholder="Describe the problem you're trying to solve..."
                className={`
                flex-1
                bg-transparent
                px-4
                py-4
                outline-none
                ${
                  darkMode
                    ? "text-white placeholder:text-slate-500"
                    : "text-slate-900 placeholder:text-slate-400"
                }
                `}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleSearch();
                  }
                }}
              />

              <button
                onClick={handleSearch}
                className="
                    flex items-center
                    cursor-pointer
                    rounded-full
                    border
                    border-transparent
                    bg-[#FFA116]
                    px-5
                    py-2.5
                    text-[15px]
                    font-bold
                    text-black
                    transition-all
                    duration-200
                    hover:bg-[#FFA116]
                    active:scale-95
                    group
                    "
              >
                Search
                <ArrowRight
                  className="
                  ml-2.5
                  w-[22px]
                  transition-transform
                  duration-300
                  ease-in-out
                  group-hover:translate-x-[5px]
                  "
                />
              </button>
            </div>
            {/* Display results */}
            {!loading &&
              (requiredConcepts.length > 0 ||
                supportingConcepts.length > 0) && (
                <div className="mt-8">
                  <p
                    className={`mb-3 text-sm font-semibold ${
                      darkMode ? "text-slate-300" : "text-slate-600"
                    }`}
                  >
                    Detected concepts
                  </p>

                  <div className="flex flex-wrap justify-center gap-2">
                    {requiredConcepts.map((concept) => (
                      <span
                        key={`required-${concept}`}
                        className="
              rounded-full
              bg-[#FFA116]/15
              px-3
              py-1.5
              text-sm
              font-semibold
              text-[#FFA116]
            "
                      >
                        {concept}
                      </span>
                    ))}

                    {supportingConcepts.map((concept) => (
                      <span
                        key={`supporting-${concept}`}
                        className={`rounded-full px-3 py-1.5 text-sm ${
                          darkMode
                            ? "bg-white/10 text-slate-300"
                            : "bg-slate-100 text-slate-600"
                        }`}
                      >
                        {concept}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            {/* Display loading */}
            {loading && (
              <p
                className={`mt-10 text-center ${
                  darkMode ? "text-slate-400" : "text-slate-500"
                }`}
              >
                Finding relevant LeetCode problems...
              </p>
            )}

            {/* Display errors */}
            {error && <p className="mt-8 text-center text-red-500">{error}</p>}
            {/* Display leetcode questions */}
            {!loading && results.length > 0 && (
              <div className="mt-10 space-y-4 text-left">
                <h2
                  className={`text-2xl font-bold ${
                    darkMode ? "text-white" : "text-slate-900"
                  }`}
                >
                  Relevant Problems
                </h2>

                {results.map((result) => (
                  <div
                    key={result.url}
                    className={`rounded-2xl border p-6 transition-all ${
                      darkMode
                        ? "border-slate-700 bg-[#111111] hover:border-slate-500"
                        : "border-slate-200 bg-white hover:border-slate-300"
                    }`}
                  >
                    <div className="flex items-center justify-between gap-4">
                      <h3
                        className={`text-xl font-semibold ${
                          darkMode ? "text-white" : "text-slate-900"
                        }`}
                      >
                        {result.title}
                      </h3>

                      <span
                        className="
              shrink-0
              rounded-full
              bg-[#FFA116]/15
              px-3
              py-1
              text-sm
              font-semibold
              text-[#FFA116]
            "
                      >
                        {result.difficulty}
                      </span>
                    </div>

                    <p
                      className={`mt-2 text-sm ${
                        darkMode ? "text-slate-400" : "text-slate-500"
                      }`}
                    >
                      Relevance score: {result.score.toFixed(2)}
                    </p>

                    <div className="mt-4 flex flex-wrap gap-2">
                      {result.matched_concepts.map((concept) => (
                        <span
                          key={`${result.title}-${concept.name}`}
                          className={`rounded-full px-3 py-1 text-sm ${
                            darkMode
                              ? "bg-white/10 text-slate-300"
                              : "bg-slate-100 text-slate-600"
                          }`}
                        >
                          {concept.name}
                        </span>
                      ))}
                    </div>

                    <a
                      href={result.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="
            mt-5
            inline-flex
            items-center
            font-semibold
            text-[#FFA116]
            transition-opacity
            hover:opacity-75
          "
                    >
                      Open on LeetCode
                      <ArrowRight size={18} className="ml-2" />
                    </a>
                  </div>
                ))}
              </div>
            )}

            {/* Handle no results */}
            {!loading && !error && query.trim() && results.length === 0 && (
              <p
                className={`mt-10 text-center ${
                  darkMode ? "text-slate-400" : "text-slate-500"
                }`}
              >
                No matching problems found.
              </p>
            )}
            {/* Suggestions */}
            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <button
                className={`
                rounded-full
                border
                px-4
                py-2
                text-sm
                shadow-sm
                transition
    ${
      darkMode
        ? `
          border-slate-700
          bg-[#111111]
          text-slate-300
          hover:border-slate-500
        `
        : `
          border-slate-300
          bg-white
          text-slate-600
          hover:border-slate-400
        `
    }
  `}
              >
                Two Sum
              </button>

              <button
                className={`
    rounded-full
    border
    px-4
    py-2
    text-sm
    shadow-sm
    transition
    ${
      darkMode
        ? `
          border-slate-700
          bg-[#111111]
          text-slate-300
          hover:border-slate-500
        `
        : `
          border-slate-300
          bg-white
          text-slate-600
          hover:border-slate-400
        `
    }
  `}
              >
                Sliding Window
              </button>

              <button
                className={`
    rounded-full
    border
    px-4
    py-2
    text-sm
    shadow-sm
    transition
    ${
      darkMode
        ? `
          border-slate-700
          bg-[#111111]
          text-slate-300
          hover:border-slate-500
        `
        : `
          border-slate-300
          bg-white
          text-slate-600
          hover:border-slate-400
        `
    }
  `}
              >
                Dynamic Programming
              </button>
            </div>
          </div>

          {/* Bottom hint */}
          <p className="mt-12 text-sm text-slate-500">
            Try describing an algorithm, data structure, or problem concept.
          </p>
        </div>
      </main>
    </div>
  );
}
