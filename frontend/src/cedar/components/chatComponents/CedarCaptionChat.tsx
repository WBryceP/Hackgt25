import React, { useCallback } from "react";
import { FloatingContainer } from "@/cedar/components/structural/FloatingContainer";
import { ChatInput } from "@/cedar/components/chatInput/ChatInput";
import Container3D from "@/cedar/components/containers/Container3D";
import CaptionMessages from "@/cedar/components/chatMessages/CaptionMessages";
import { KeyboardShortcut } from "@/cedar/components/ui/KeyboardShortcut";
import {
  Bug,
  CheckCircle,
  History,
  Package,
  Settings,
  XCircle,
  Undo,
  Redo,
} from "lucide-react";
import Container3DButton from "@/cedar/components/containers/Container3DButton";

interface CedarCaptionChatProps {
  dimensions?: {
    width?: number;
    maxWidth?: number;
  };
  className?: string;
  showThinking?: boolean;
  stream?: boolean; // Whether to use streaming for responses
}

export const CedarCaptionChat: React.FC<CedarCaptionChatProps> = ({
  dimensions,
  className = "",
  showThinking = true,
  stream = true,
}) => {
  return (
    <div className="text-sm">
      <div className="w-full pb-3">
        <CaptionMessages showThinking={showThinking} />
      </div>

      <ChatInput className="bg-transparent p-0" stream={stream} />
    </div>
  );
};
