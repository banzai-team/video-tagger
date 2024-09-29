import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Link } from "react-router-dom";
import { Routes } from "@/Router.tsx";
import { ArrowLeft } from "lucide-react";
import { Badge } from "@/components/ui/badge.tsx";
import { Spinner } from '@/components/ui/spinner';
import { useInferenceEndpointsServiceGetVideoByIdV1VideosIdGet } from "@/openapi/queries/queries";
import { InferenceEndpointsService } from "@/openapi/requests/services.gen";
import { useQuery } from "@tanstack/react-query";
import { Skeleton } from '@/components/ui/skeleton';

const VideoPage: React.FC = () => {
  const { id = '' } = useParams();
  const successStatuses = ['DOWNLOADED', 'AUDIO_EXTRACTED']

  const { data } = useQuery({
    queryKey: [useInferenceEndpointsServiceGetVideoByIdV1VideosIdGet],
    queryFn: () => InferenceEndpointsService.getVideoByIdV1VideosIdGet({ id }),
    // refetchInterval: 3000,
    refetchInterval: data => !successStatuses.includes(data?.state?.data?.status) ? 3000 : false,
  });

  const tags = data?.tags ? JSON.parse(data?.tags) : []

  return (
    <>
      <Link
        to={Routes.Root}
        className="flex gap-2 items-center text-xs text-gray-400 hover:text-gray-500"
      >
        <ArrowLeft className="h-3 w-3" />вернуться на главную
      </Link>
      <h2 className="mb-5">{data?.title}</h2>
      <div className="grid grid-cols-1 gap-2 md:gap-4 md:grid-cols-2">
        {/*TODO: fix video size. Link or video file??? Check on correct data*/}
        {!data?.video_path ? <Skeleton className="h-80 w-full rounded-3xl" /> : <iframe
          className="w-full h-96"
          src={`http://api.localhost/${data?.video_path}`}
          frameBorder="0"
          allow="clipboard-write"
        // webkitAllowFullScreen
        // mozallowfullscreen
        // allowFullScreen
        />}
        <div>
          <div className="flex gap-3 flex-wrap max-h-max">
            {!data?.tags ? <>
              <div className='flex gap-5 align-center justify-center w-full'>
                <div className="font-bold">Теги:</div>
                <Skeleton className="h-4 w-full self-center" />
              </div>
            </> : <>
              <div className="font-bold">Теги:</div>
              {tags.map((tag, key) => (
                <Badge key={`video-tag-${key}`} variant="accent">{tag}</Badge>
              ))}
            </>
            }
          </div>
          <div className="pt-5 flex gap-3 flex-wrap md:pt-10">
            {!data?.description
              ? <div className='flex flex-col gap-2 w-full'>
                <div className='flex gap-5 align-center justify-center'>
                  <div className="font-bold">Описание: </div>
                  <Skeleton className="h-4 w-full self-center" />
                </div>
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 max-w-[400px] w-full" />
              </div>
              : <>
                <div className="font-bold">Описание: </div>
                <div className="text-gray-500">{data?.description}</div>
              </>
            }
          </div>
        </div>
      </div >
    </>
  );
};

export default VideoPage;
