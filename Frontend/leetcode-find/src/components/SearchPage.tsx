import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Home, ArrowRight, Moon, Sun, Search } from "lucide-react";
import Loader from "./Loader";

interface SearchPageProps {
  darkMode: boolean;
  setDarkMode: React.Dispatch<React.SetStateAction<boolean>>;
}

export default function SearchPage({
  darkMode,
  setDarkMode,
}: SearchPageProps) {

  const navigate = useNavigate();
  const [query, setQuery] = useState("");


  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
  if (!query.trim()) {
    return;
  }

  setLoading(true);
  setError("");

  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/search`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query.trim(),
        }),
      }
    );

    if (!response.ok) {
      throw new Error("Search request failed.");
    }

    const data = await response.json();

    navigate("/results", {
      state: {
        ...data,
        query: query.trim(),
      },
    });
  } catch (err) {
    console.error(err);
    setError("Could not connect to the search server.");
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
    {loading ? (
      /* =========================
         LOADING SCREEN
         ========================= */
      <div className="flex min-h-screen items-center justify-center px-6">
        <div className="text-center">
          <Loader />

          <h2
            className={`
              mt-8
              text-2xl
              font-thin
              ${
                darkMode
                  ? "text-white"
                  : "text-slate-900"
              }
            `}
          >
            Finding relevant problems...
          </h2>

        </div>
      </div>
    ) : (
      <>
        {/* =========================
            NAVBAR
            ========================= */}

        <nav className="flex items-center justify-between px-10 py-6">
          {/* Logo */}
          <div
            className={`text-xl font-Kanit font-medium text-[1.125rem] text-black ${
              darkMode
                ? "text-white"
                : "text-slate-900"
            }`}
          >
            LeetCodeFind
          </div>

          {/* Right side */}
          <div className="flex items-center gap-3">
            {/* Home */}
            <button
              onClick={() => navigate("/")}
              className={`
                group
                flex
                items-center
                gap-1.5
                transition-colors
                duration-200
                ${
                  darkMode
                    ? "text-white hover:text-white"
                    : "text-slate-600 hover:text-black"
                }
              `}
            >
              <Home
                size={18}
                className="transition-colors duration-200"
              />

              <span>
                Home
              </span>
            </button>

            {/* Brightness toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className={`
                rounded-full
                p-2
                transition-colors
                duration-200
                ${
                  darkMode
                    ? "text-white hover:bg-white/10"
                    : "text-gray-700 hover:bg-black/5"
                }
              `}
            >
              {darkMode ? (
                <Sun size={18} />
              ) : (
                <Moon size={18} />
              )}
            </button>
          </div>
        </nav>

        {/* =========================
            MAIN SEARCH SECTION
            ========================= */}

        <main className="flex min-h-[calc(100vh-100px)] items-center justify-center px-6">
          <div className="w-full max-w-3xl text-center">

            {/* Heading */}
            <div className="mb-10">
              <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-[#FFA116]">
                Intelligent Problem Search
              </p>

              <h1
                className={`
                  text-5xl
                  font-bold
                  tracking-tight
                  ${
                    darkMode
                      ? "text-white"
                      : "text-slate-900"
                  }
                `}
              >
                Find the right
                <span className="text-[#FFA116]">
                  {" "}
                  LeetCode problem 
                </span>
              </h1>

              <p
                className={`
                  mx-auto
                  mt-5
                  max-w-xl
                  text-lg
                  leading-8
                  ${
                    darkMode
                      ? "text-slate-300"
                      : "text-slate-600"
                  }
                `}
              >
                Describe the concept you're trying to solve
                and discover relevant LeetCode questions using
                semantic search.
              </p>
            </div>

            {/* Search Box */}
            <div className="mx-auto max-w-2xl">
              <div
                className={`
                  flex
                  items-center
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
                  placeholder="Describe the concept you're looking for..."
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
                  onChange={(e) =>
                    setQuery(e.target.value)
                  }
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handleSearch();
                    }
                  }}
                />

                <button
                  onClick={handleSearch}
                  disabled={loading}
                  className="
                    group
                    flex
                    cursor-pointer
                    items-center
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
                    disabled:cursor-not-allowed
                    disabled:opacity-60
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

              {/* Error */}
              {error && (
                <p className="mt-8 text-center text-red-500">
                  {error}
                </p>
              )}

              {/* Suggestions */}
              <div className="mt-6 flex flex-wrap justify-center gap-3">
                <button
                  onClick={() =>
                    setQuery("Mirror Index")
                  }
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
                  Mirror Index
                </button>

                <button
                  onClick={() =>
                    setQuery("Math")
                  }
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
                  Math
                </button>

                <button
                  onClick={() =>
                    setQuery("Dynamic Programming")
                  }
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
            
          </div>
        </main>
      </>
    )}
  </div>
);
}
