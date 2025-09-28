import { useEffect, useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import useDownloadVideo from "../functions/downloadVideoPipeline";
import Loader from "../components/general/Loader";
import YouTube from "react-youtube";
import SectionTabs from "../components/video/SectionTabs";
import DeepSearch from "../components/video/sections/DeepSearch";
import { useRegisterState, useRegisterFrontendTool } from "cedar-os";
import { z } from "zod";

const POLL_MS = 500;

const Video = ({ setError }) => {
  const { id } = useParams();

  const playerRef = useRef(null);
  const pendingSeekRef = useRef(null);

  const [currentTime, setCurrentTime] = useState(0);

  useRegisterState({
    key: "videoTimeStamp",
    description: "current timestamp of the youtube video",
    value: currentTime,
    setValue: setCurrentTime,
    stateSetters: {
      setTime: {
        name: "setTime",
        description: "Seek the YouTube player to a time in seconds",
        argsSchema: z.object({
          seconds: z.number().nonnegative().optional(),
          play: z.boolean().optional(),
        }),
        execute: async (_currentState, args) => {
          const seconds = Number(args?.seconds);
          const play = Boolean(args?.play);
          if (!Number.isFinite(seconds) || seconds < 0) return;

          const player = playerRef.current;
          if (!player) return;
          player.seekTo(seconds, true);
          if (play) player.playVideo();
          setCurrentTime(seconds);
        },
      },
    },
  });

  // Frontend tool too:
  useRegisterFrontendTool({
    name: "seekYoutube",
    description: "Seek the embedded YouTube player",
    // ✅ Minimal schema (loose)
    argsSchema: z.object({
      seconds: z.number().nonnegative().optional(),
      play: z.boolean().optional(),
    }),
    execute: async ({ seconds, play }) => {
      const s = Number(seconds);
      if (!Number.isFinite(s) || s < 0) return;

      const player = playerRef.current;
      if (!player) return;
      player.seekTo(s, true);
      if (play) player.playVideo();
      setCurrentTime(s);
    },
  });

  const onReady = (e) => {
    playerRef.current = e.target;
    e.target.pauseVideo();

    // flush any queued seek
    const pending = pendingSeekRef.current;
    if (pending) {
      e.target.seekTo(pending.seconds, true);
      if (pending.play) e.target.playVideo();
      setCurrentTime(pending.seconds);
      pendingSeekRef.current = null;
    }
  };

  const seekFunction = (start) => {
    playerRef.current.seekTo(start, true);
  };

  useEffect(() => {
    const tick = () => {
      const t = playerRef.current?.getCurrentTime?.();
      if (typeof t === "number" && !Number.isNaN(t)) setCurrentTime(t);
    };
    const id = setInterval(tick, POLL_MS);
    return () => clearInterval(id);
  }, []);

  return (
    <div>
      <div className="flex flex-col md:flex-row gap-2">
        {/* VIDEO */}
        <div className="w-full flex flex-col">
          <YouTube
            className="w-full aspect-video"
            iframeClassName="w-full h-full"
            videoId={id}
            opts={{
              width: "100%",
              height: "100%",
              playerVars: {
                autoplay: 0,
                controls: 1,
                rel: 0,
                modestbranding: 1,
                fs: 0,
              },
            }}
            onReady={onReady}
          />

          <div className="hidden md:block grow">
            <DeepSearch />
          </div>
        </div>

        {/* Tabs */}
        <SectionTabs setError={setError} id={id} seekFunction={seekFunction} />
      </div>
    </div>
  );
};

export default Video;
