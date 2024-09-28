// generated with @7nohe/openapi-react-query-codegen@1.6.1 

import { type QueryClient } from "@tanstack/react-query";
import { InferenceEndpointsService, SystemProbsService } from "../requests/services.gen";
import * as Common from "./common";
export const prefetchUseInferenceEndpointsServiceGetVideoByIdV1VideosIdGet = (queryClient: QueryClient, { id }: {
  id: unknown;
}) => queryClient.prefetchQuery({ queryKey: Common.UseInferenceEndpointsServiceGetVideoByIdV1VideosIdGetKeyFn({ id }), queryFn: () => InferenceEndpointsService.getVideoByIdV1VideosIdGet({ id }) });
export const prefetchUseInferenceEndpointsServiceGetVideosV1VideosGet = (queryClient: QueryClient, { size, skip }: {
  size?: unknown;
  skip?: unknown;
} = {}) => queryClient.prefetchQuery({ queryKey: Common.UseInferenceEndpointsServiceGetVideosV1VideosGetKeyFn({ size, skip }), queryFn: () => InferenceEndpointsService.getVideosV1VideosGet({ size, skip }) });
export const prefetchUseSystemProbsServiceHealthHealthGet = (queryClient: QueryClient) => queryClient.prefetchQuery({ queryKey: Common.UseSystemProbsServiceHealthHealthGetKeyFn(), queryFn: () => SystemProbsService.healthHealthGet() });
