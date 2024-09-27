// generated with @7nohe/openapi-react-query-codegen@1.6.1 

import { type QueryClient } from "@tanstack/react-query";
import { SystemProbsService, VideoManagementService } from "../requests/services.gen";
import * as Common from "./common";
export const prefetchUseVideoManagementServiceListVideosV1ListVideosGet = (queryClient: QueryClient) => queryClient.prefetchQuery({ queryKey: Common.UseVideoManagementServiceListVideosV1ListVideosGetKeyFn(), queryFn: () => VideoManagementService.listVideosV1ListVideosGet() });
export const prefetchUseSystemProbsServiceHealthHealthGet = (queryClient: QueryClient) => queryClient.prefetchQuery({ queryKey: Common.UseSystemProbsServiceHealthHealthGetKeyFn(), queryFn: () => SystemProbsService.healthHealthGet() });
