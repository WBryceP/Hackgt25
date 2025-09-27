import { useEffect } from "react";
import { useParams } from "react-router-dom";

import SectionTabs from "../components/video/SectionTabs";

const Video = () => {
  const { id } = useParams();

  useEffect(() => {
    console.log(id);
  }, [id]);

  return (
    <div className="flex flex-col md:flex-row gap-2">
      {/* VIDEO */}
      <div className="w-full bg-primaryInvert aspect-square rounded-sm" />
      {/* Tabs */}
      <SectionTabs />
    </div>
  );
};

export default Video;
