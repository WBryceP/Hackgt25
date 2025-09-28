import { useState, useEffect } from "react";
import ClaimAnswer from "./sections/ClaimAnswer";
import DeepSearch from "./sections/DeepSearch";
import Loader from "../general/Loader";
import FlaggedMoments from "./sections/FlaggedMoments";
import {
  useRegisterState,
  useStateBasedMentionProvider,
  useSubscribeStateToAgentContext,
} from "cedar-os";
import { useNavigate } from "react-router-dom";
import useDownloadVideo from "../../functions/downloadVideoPipeline";

const SectionTabs = ({ id, setError }) => {
  const nav = useNavigate();

  const [selectedTab, setSelectedTab] = useState(1);
  const [flaggedMoments, setFlaggedMoments] = useState([
    {
      momentName: "USA has the best economy",
      momentContext: "USA es numero uno",
    },
  ]);

  const [claimsAnswers, setClaimsAnswers] = useState([]);

  const [
    downloadVideo,
    downloadVideoResult,
    downloadError,
    loading,
    setDownloadVideoResult,
  ] = useDownloadVideo();

  useEffect(() => {
    downloadVideo("https://www.youtube.com/watch?v=" + id);
  }, [id]);

  useEffect(() => {
    if (downloadVideoResult?.length > 0) {
      console.log(downloadVideoResult?.factCheck);
      console.log(downloadVideoResult?.clip);
      setClaimsAnswers(downloadVideoResult.map((item) => item.factCheck));
      setFlaggedMoments(downloadVideoResult.map((item) => item.clip));

      setDownloadVideoResult(null);
    }
  }, [downloadVideoResult]);

  useEffect(() => {
    if (downloadError.length > 0) {
      setError(downloadError); // if setError expects a string, pass a message instead
      nav("/error");
    }
  }, [downloadError, nav, setError]);

  const tabs = [
    { name: "Search", shortened: "Search" },
    { name: "Claim & Answer", shortened: "Claim" },
    { name: "Flagged Moments", shortened: "Moments" },
    // { name: "Sources", shortened: "Sources" },
  ];

  const content = [
    <DeepSearch />,
    <ClaimAnswer
      claimsAnswers={claimsAnswers}
      setClaimAnswers={setClaimsAnswers}
    />,
    <FlaggedMoments
      flaggedMoments={flaggedMoments}
      setFlaggedMoments={setFlaggedMoments}
    />,
    // <Sources sources={sources} setSources={sources} />,
  ];

  // Claims
  useRegisterState({
    key: "claimsAnswers",
    description: "claims made by politicians (that may be true or false)",
    value: claimsAnswers,
  });
  useStateBasedMentionProvider({
    stateKey: "claimsAnswers",
    trigger: "@",
    labelField: "claim",
    order: 10,
    description: "Claims",
    icon: "🔎",
    color: "#b6dc76",
  });

  // Flagged Moments
  useRegisterState({
    key: "flaggedMoments",
    description:
      "important moments where a politican has made a claim (that may either be true or false)",
    value: flaggedMoments,
  });
  useStateBasedMentionProvider({
    stateKey: "flaggedMoments",
    trigger: "@",
    labelField: "momentName",
    order: 10,
    description: "Moments",
    icon: "🔎",
    color: "#eec643",
  });

  useSubscribeStateToAgentContext({
    stateKey: "claimsAnswers",
    name: "Claims & Answers",
    // keep payload compact so it fits in context
    select: (claimsAnswers) =>
      claimsAnswers
        .map((c) => ({
          claim: c.claim,
          confidence: c.confidence,
          sources: c.sources?.slice(0, 3),
        }))
        .slice(0, 10),
  });

  useSubscribeStateToAgentContext({
    stateKey: "flaggedMoments",
    name: "Flagged Moments",
    select: (flaggedMoments) =>
      flaggedMoments
        .map((m) => ({
          momentName: m.momentName,
          momentContext: m.momentContext,
        }))
        .slice(0, 20),
  });

  // Sources
  // useRegisterState({
  //   key: "sources",
  //   description:
  //     "a list of sources that provide context to claims made by politicians (and whether or not their statements are true)",
  //   value: sources,
  //   setValue: setSources,
  // });
  // useStateBasedMentionProvider({
  //   stateKey: "sources",
  //   trigger: "@",
  //   labelField: "sourceName",
  //   order: 10,
  //   description: "Sources",
  //   icon: "🔎",
  //   color: "#3b82f6",
  // });

  const [windowWidth, setWindowWidth] = useState(0);
  const resizeFunc = () => {
    setWindowWidth(window.innerWidth);
  };

  useEffect(() => {
    setWindowWidth(window.innerWidth);
    window.addEventListener("resize", resizeFunc);

    return () => window.removeEventListener("resize", resizeFunc);
  }, []);

  useEffect(() => {
    setSelectedTab(windowWidth > 768 ? 1 : 0);
  }, [windowWidth]);

  const TabComponents = tabs.map((tab, index) => {
    return (
      <li
        className={`relative flex flex-1  justify-center items-center hover:bg-primaryInvert/20 py-2 cursor-pointer rounded-sm ${
          selectedTab === index ? "bg-body font-semibold" : null
        }`}
        key={index}
        onClick={() => setSelectedTab(index)}
      >
        <h2 className="text-center ">{tab.name}</h2>
        {selectedTab === index ? (
          <hr className="w-full absolute bottom-0 border-1" />
        ) : null}
      </li>
    );
  });

  return (
    <div className="bg-primary shadow-md rounded-md md:w-[50%]">
      {/* Formats */}

      <ul className="md:hidden flex flex-row w-full justify-between">
        {TabComponents}
      </ul>
      <ul className="hidden md:flex flex-row w-full justify-between">
        {TabComponents.slice(1, TabComponents.length)}
      </ul>
      {loading ? (
        <div className="w-full h-1/3 flex justify-center items-center">
          <Loader />
        </div>
      ) : downloadError.length > 0 ? (
        <div className="text-lowText text-center text-2xl h-1/3 justify-center items-center flex">
          There was an error while retrieving your video
        </div>
      ) : (
        <>
          <div className="hidden md:flex p-2 relative   overflow-scroll ">
            {content[selectedTab]}
          </div>
          <div className="flex md:hidden p-2 relative  overflow-scroll">
            {content[selectedTab]}
          </div>
        </>
      )}
    </div>
  );
};

export default SectionTabs;
