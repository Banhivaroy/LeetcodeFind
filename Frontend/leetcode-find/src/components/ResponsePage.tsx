import { useLocation, useNavigate } from "react-router-dom";
import { ArrowLeft, ArrowRight, ExternalLink, Search } from "lucide-react";

interface MatchedConcept {
  name: string;
  category: string;
  parent?: string | null;
}

interface ProblemResult {
  score: number;
  title: string;
  difficulty: string;
  url: string;
  matched_concepts: MatchedConcept[];
}

interface ConceptPath {
  concept: string;
  category: string;
  path: string[];
}

interface SearchResponse {
  query: string;
  required_concepts: string[];
  supporting_concepts: string[];
  concept_paths?: ConceptPath[];
  results?: ProblemResult[];
}

export default function ResponsePage() {
  const location = useLocation();
  const navigate = useNavigate();

  const data = location.state as SearchResponse | null;

  // --------------------------------------------------
  // No search data
  // --------------------------------------------------

  if (!data) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black px-6 text-white">
        <div className="text-center">
          <Search size={40} className="mx-auto mb-5 text-[#FFA116]" />

          <h1 className="text-2xl font-bold">No search results</h1>

          <p className="mt-2 text-slate-400">
            Start a search to find relevant LeetCode problems.
          </p>

          <button
            onClick={() => navigate("/")}
            className="
              mt-6
              inline-flex
              items-center
              gap-2
              rounded-full
              bg-[#FFA116]
              px-5
              py-2.5
              font-semibold
              text-black
              transition
              hover:bg-[#ffae2f]
              active:scale-95
            "
          >
            <ArrowLeft size={18} />
            Back to Search
          </button>
        </div>
      </div>
    );
  }

  const conceptPaths = data.concept_paths ?? [];
  const results = data.results ?? [];

  // --------------------------------------------------
  // Remove duplicate concept paths
  // --------------------------------------------------

  const uniqueConceptPaths = conceptPaths.filter(
    (conceptPath, index, paths) => {
      const currentPath = conceptPath.path.join(">");
      const firstIndex = paths.findIndex(
        (path) => path.path.join(">") === currentPath,
      );

      return firstIndex === index;
    },
  );

  return (
    <div
      className="
        min-h-screen
        bg-black
        text-white
        [background-image:linear-gradient(to_right,_rgba(255,_255,_255,_0.12)_1px,_transparent_1px),_linear-gradient(to_bottom,_rgba(255,_255,_255,_0.12)_1px,_transparent_1px)]
        [background-size:35px_35px]
      "
    >
      {/* --------------------------------------------------
          Navbar
      -------------------------------------------------- */}

      <nav className="flex items-center justify-between px-8 py-6 md:px-12">
        <div className="text-xl font-bold">LeetCodeFind</div>

        <button
          onClick={() => navigate("/search")}
          className="
            flex
            items-center
            gap-2
            text-sm
            text-slate-300
            transition
            hover:text-white
          "
        >
          <ArrowLeft size={18} />
          New Search
        </button>
      </nav>

      {/* --------------------------------------------------
          Main
      -------------------------------------------------- */}

      <main className="mx-auto w-full max-w-6xl px-6 pb-20">
        {/* --------------------------------------------------
            Search query
        -------------------------------------------------- */}

        <section className="pt-8 text-center">
          <h1
            className="
              mx-auto
              max-w-5xl
              text-4xl
              font-bold
              leading-tight
              tracking-tight
              md:text-5xl
            "
          >
            {data.query}
          </h1>
        </section>

        {/* --------------------------------------------------
          Detected Concepts
          -------------------------------------------------- */}

        {uniqueConceptPaths.length > 0 && (
          <section className="mt-10">
            <h2 className="mb-6 text-lg font-semibold">Detected Concepts :</h2>

            {/* Main parent / root concepts */}
            <div className="mb-8 flex flex-wrap justify-center gap-6">
              {uniqueConceptPaths
                .filter((conceptPath) => conceptPath.path.length === 1)
                .map((conceptPath) => {
                  const rootConcept =
                    conceptPath.path[0] ?? conceptPath.concept;

                  const displayName =
                    rootConcept.charAt(0).toUpperCase() + rootConcept.slice(1);

                  return (
                    <span
                      key={conceptPath.concept}
                      className="
            text-2xl
            font-bold
            text-[#FFA116]
          "
                    >
                      {displayName}
                    </span>
                  );
                })}
            </div>

            {/* Child concept flows */}
            <div className="space-y-5">
              {uniqueConceptPaths
                .filter((conceptPath) => conceptPath.path.length > 1)
                .map((conceptPath, pathIndex) => (
                  <div
                    key={`${conceptPath.concept}-${pathIndex}`}
                    className="
              flex
              flex-wrap
              items-center
              justify-center
              gap-3
            "
                  >
                    {conceptPath.path.map((concept, index) => {
                      const isLast = index === conceptPath.path.length - 1;

                      return (
                        <div
                          key={`${conceptPath.concept}-${concept}-${index}`}
                          className="flex items-center gap-3"
                        >
                          <span
                            className={`
                      rounded-full
                      border
                      px-4
                      py-2
                      text-sm
                      font-medium
                      transition-colors
                      ${
                        isLast
                          ? `
                            border-[#FFA116]/30
                            bg-[#FFA116]/15
                            text-[#FFA116]
                          `
                          : `
                            border-slate-700
                            bg-[#111111]
                            text-slate-300
                          `
                      }
                    `}
                          >
                            {concept}
                          </span>

                          {!isLast && (
                            <ArrowRight
                              size={20}
                              strokeWidth={2}
                              className="text-slate-500"
                            />
                          )}
                        </div>
                      );
                    })}
                  </div>
                ))}
            </div>
          </section>
        )}

        {/* --------------------------------------------------
            Results
        -------------------------------------------------- */}

        <section className="mt-12">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-2xl font-bold md:text-3xl">
              Relevant Problems
            </h2>

            <span className="text-sm text-slate-500">
              {results.length} {results.length === 1 ? "problem" : "problems"}
            </span>
          </div>

          {/* --------------------------------------------------
              No results
          -------------------------------------------------- */}

          {results.length === 0 ? (
            <div
              className="
                rounded-2xl
                border
                border-slate-800
                bg-[#0d0d0d]
                px-6
                py-14
                text-center
              "
            >
              <Search size={36} className="mx-auto mb-4 text-slate-500" />

              <h3 className="text-xl font-semibold">
                No matching problems found
              </h3>

              <p className="mt-2 text-slate-500">
                Try describing the algorithm, pattern, or technique differently.
              </p>

              <button
                onClick={() => navigate("/")}
                className="
                  mt-6
                  rounded-full
                  bg-[#FFA116]
                  px-5
                  py-2.5
                  font-semibold
                  text-black
                  transition
                  hover:bg-[#ffae2f]
                  active:scale-95
                "
              >
                Try Another Search
              </button>
            </div>
          ) : (
            <div className="space-y-5">
              {results.map((result, index) => (
                <article
                  key={`${result.url}-${index}`}
                  className="
                    rounded-2xl
                    border
                    border-slate-800
                    bg-[#111111]
                    p-6
                    shadow-lg
                    transition-all
                    duration-200
                    hover:-translate-y-0.5
                    hover:border-slate-600
                    hover:shadow-2xl
                    md:p-7
                  "
                >
                  {/* Top row */}

                  <div
                    className="
                      flex
                      flex-col
                      gap-5
                      md:flex-row
                      md:items-start
                      md:justify-between
                    "
                  >
                    <div className="flex items-start gap-4">
                      {/* Rank */}

                      <div
                        className="
                          flex
                          h-10
                          w-10
                          shrink-0
                          items-center
                          justify-center
                          rounded-full
                          bg-white/8
                          text-sm
                          font-bold
                          text-slate-300
                        "
                      >
                        #{index + 1}
                      </div>

                      {/* Problem information */}

                      <div>
                        <h3 className="text-xl font-bold md:text-2xl">
                          {result.title}
                        </h3>

                        <p className="mt-2 text-sm text-slate-400">
                          Relevance score:{" "}
                          <span className="text-slate-300">
                            {result.score.toFixed(2)}
                          </span>
                        </p>
                      </div>
                    </div>

                    {/* Difficulty */}

                    <span
                      className="
                        w-fit
                        shrink-0
                        rounded-full
                        bg-[#FFA116]/15
                        px-4
                        py-2
                        text-sm
                        font-semibold
                        text-[#FFA116]
                      "
                    >
                      {result.difficulty}
                    </span>
                  </div>

                  {/* Matched concepts */}

                  {result.matched_concepts.length > 0 && (
                    <div className="mt-6">
                      <div className="flex flex-wrap gap-2">
                        {result.matched_concepts.map(
                          (concept, conceptIndex) => (
                            <span
                              key={`${result.url}-${concept.name}-${conceptIndex}`}
                              className="
                                rounded-full
                                bg-white/8
                                px-3
                                py-1.5
                                text-sm
                                text-slate-300
                              "
                            >
                              {concept.name}
                            </span>
                          ),
                        )}
                      </div>
                    </div>
                  )}

                  {/* LeetCode link */}

                  <div className="mt-7">
                    <a
                      href={result.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="
                        inline-flex
                        items-center
                        gap-2
                        font-semibold
                        text-[#FFA116]
                        transition
                        hover:text-[#ffb340]
                      "
                    >
                      Open on LeetCode
                      <ExternalLink size={18} />
                    </a>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
