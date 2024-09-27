import React from 'react';
import {VideoDataItem} from "@/pages/MainPage/MainPage.tsx";

type VideoTableProps = {
    data: VideoDataItem[];
};

const VideoTable: React.FC<VideoTableProps> = ({data}) => {
    return (
        <div>
            {data.map((item, key) => <div key={`video-${key}`}>video - {item.name}</div>)}
        </div>
    );
};

export default VideoTable;
