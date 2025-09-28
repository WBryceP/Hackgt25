import { useEffect } from "react";
import { useParams } from "react-router-dom";
import useDownloadVideo from "../functions/downloadVideoPipeline";
import Loader from "../components/general/Loader";
import { useNavigate } from "react-router-dom";

import SectionTabs from "../components/video/SectionTabs";
import DeepSearch from "../components/video/sections/DeepSearch";

const Video = ({ setError }) => {
  const { id } = useParams();
  const nav = useNavigate();
  const [downloadVideo, downloadError, loading] = useDownloadVideo();

  useEffect(() => {
    downloadVideo(`https://www.youtube.com/watch?v=${id}`);
  }, [id]);

  useEffect(() => {
    if (downloadError === true) {
      setError(downloadError);
      nav("/error");
    }
  }, [downloadError]);

  return (
    <div>
      <a
        className="block font-semibold text-xl mb-4 w-fit"
        href={`https://www.youtube.com/watch?v=${id}`}
        target="_blank"
      >
        https://www.youtube.com/watch?v={id}
      </a>
      <div className="flex flex-col md:flex-row gap-2">
        {/* VIDEO */}
        <div className=" w-full md:h-[90vh]  flex flex-col">
          <div className="w-full bg-primaryInvert aspect-video rounded-sm mb-2 justify-center flex items-center">
            <Loader />
          </div>
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
