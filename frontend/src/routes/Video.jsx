import { useEffect } from "react";
import { useParams } from "react-router-dom";

const Video = () => {
  const { id } = useParams();

  useEffect(() => {
    console.log(id);
  }, [id]);

  return (
    <div className="flex flex-col gap-2">
      {/* VIDEO */}
      <div className="w-full bg-primaryInvert aspect-square rounded-sm" />
    </div>
  );
};

export default Video;
