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
    // downloadVideo(`https://www.youtube.com/watch?v=${id}`);
  }, [id]);

  useEffect(() => {
    if (downloadError === true) {
      setError(downloadError);
      nav("/error");
    }
  }, [downloadError]);

  return (
    <div className="">
      <div className="flex flex-col md:flex-row gap-2">
        {/* VIDEO */}

        <div className=" w-full  flex flex-col">
          <iframe
            className="w-full aspect-video"
            src={`https://www.youtube.com/embed/${id}`}
            title="YouTube video player"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen={false}
          ></iframe>

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
