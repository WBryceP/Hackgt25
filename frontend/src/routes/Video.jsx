import { useEffect } from "react";
import { useParams } from "react-router-dom";

import SectionTabs from "../components/video/SectionTabs";
import DeepSearch from "../components/video/sections/DeepSearch";

const Video = () => {
  const { id } = useParams();

  useEffect(() => {
    console.log(id);
  }, [id]);

  return (
    <div>
      <div className="flex flex-col md:flex-row gap-2">
        {/* VIDEO */}
        <div className=" w-full md:h-[90vh]  flex flex-col">
          <div className="w-full bg-primaryInvert aspect-video rounded-sm mb-2" />
          <div className="hidden md:block grow">
            <DeepSearch />
          </div>
        </div>

        {/* Tabs */}
        <SectionTabs />
      </div>
    </div>
  );
};

export default Video;
