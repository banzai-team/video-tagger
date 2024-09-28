import React from 'react';
import { useParams } from 'react-router-dom';
import { Link } from "react-router-dom";
import { Routes } from "@/Router.tsx";
import { ArrowLeft } from "lucide-react";
import { Badge } from "@/components/ui/badge.tsx";

import { useInferenceEndpointsServiceGetVideoByIdV1VideosIdGet } from "@/openapi/queries";

const VideoPage: React.FC = () => {
  const { id = '' } = useParams();

  const { data } = useInferenceEndpointsServiceGetVideoByIdV1VideosIdGet({ id });

  const tags = data?.tags ? JSON.parse(data?.tags) : []

  return (
    <>
      <Link
        to={Routes.Root}
        className="flex gap-2 items-center text-xs text-gray-400 hover:text-gray-500"
      >
        <ArrowLeft className="h-3 w-3" />вернуться на главную
      </Link>
      {/*todo: name of video instead ?*/}
      <h2 className="mb-5">{data?.title}</h2>
      <div className="grid grid-cols-1 gap-2 md:gap-4 md:grid-cols-2">
        {/*TODO: fix video size. Link or video file??? Check on correct data*/}
        <iframe
          className="w-full h-96"
          src={`http://api.localhost/${data?.video_path}`}
          frameBorder="0"
          allow="clipboard-write; autoplay"
        // webkitAllowFullScreen
        // mozallowfullscreen
        // allowFullScreen
        />
        <div>
          <div className="flex gap-3 flex-wrap max-h-max">
            {
              tags.map((tag, key) => (
                <Badge key={`video-tag-${key}`} variant="accent">{tag}</Badge>
              ))
            }
          </div>
          <div className="pt-5  flex gap-1 flex-wrap md:pt-10">
            <div className="font-bold">Описание:</div>
            <div className="text-gray-500">{data?.description}</div>
          </div>
        </div>
      </div>
    </>
  );
};

export default VideoPage;
