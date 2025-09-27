import { useState } from "react";

const SectionTabs = () => {
  const [selectedTab, setSelectedTab] = useState(1);

  const tabs = [
    { name: "Search", shortened: "Search" },
    { name: "Claim & Answer", shortened: "Claim" },
    { name: "Flagged Moments", shortened: "Moments" },
    { name: "Sources", shortened: "Sources" },
  ];

  const TabComponents = tabs.map((tab, index) => {
    return (
      <li
        className={`relative flex flex-1  justify-center items-center hover:bg-primaryInvert/20 py-2 cursor-pointer rounded-sm ${
          selectedTab === index ? "bg-body" : null
        }`}
        key={index}
        onClick={() => setSelectedTab(index)}
      >
        <h2 className="text-center text-xs sm:text-sm md:text-base">
          {tab.name}
        </h2>
        {selectedTab === index ? (
          <hr className="w-full absolute bottom-0 border-1" />
        ) : null}
      </li>
    );
  });

  return (
    <div className="bg-primary shadow-md rounded-md">
      <ul className="flex flex-row w-full justify-between">{TabComponents}</ul>
    </div>
  );
};

export default SectionTabs;
