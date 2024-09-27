import React from 'react';
import {VideoDataItem} from "@/pages/MainPage/MainPage.tsx";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import {Routes} from "@/Router";
import {Badge} from "@/components/ui/badge";

type VideoTableProps = {
    data: VideoDataItem[];
};

const VideoTable: React.FC<VideoTableProps> = ({data}) => {
    return (
        <Table>
            <TableHeader>
                <TableHead>Название</TableHead>
                <TableHead>Ссылка</TableHead>
                <TableHead>Теги</TableHead>
            </TableHeader>
            <TableBody>
                {data.map((item) => (
                    <TableRow key={`video-${item.id}`}>
                        <TableCell className="max-w-48 w-max">
                            <a href={`${Routes.Video}/${item.id}`} className="font-medium">
                                {item.name}
                            </a>
                        </TableCell>
                        <TableCell className="max-w-40 overflow-hidden text-ellipsis whitespace-nowrap">
                            <a
                                href={item.source}
                                target="_blank"
                                className="font-medium"
                            >
                                {item.source}
                            </a>
                        </TableCell>
                        <TableCell className="flex gap-2">
                            {item.tags.map(item => (
                                <Badge className="text-xs whitespace-nowrap" variant='default'>
                                    {item}
                                </Badge>)
                            )}
                        </TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    );
};

export default VideoTable;
