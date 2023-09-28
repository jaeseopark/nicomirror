import { Search2Icon } from "@chakra-ui/icons";
import {
  Input,
  InputGroup,
  InputLeftElement,
  Popover,
  PopoverArrow,
  PopoverBody,
  PopoverContent,
  PopoverTrigger,
  useDisclosure,
} from "@chakra-ui/react";
import { Link as ChakraLink } from "@chakra-ui/react";
import { forwardRef, useEffect, useMemo, useRef, useState } from "react";
import { Link as ReactRouterLink } from "react-router-dom";

import { Classification, classifySearchTerm } from "./utils/regex";

const SearchInputGroup = forwardRef(({ input, onChange }: { input: string; onChange: (newInput: string) => void }, ref: any) => (
  <InputGroup borderRadius={5} size="sm">
    <InputLeftElement pointerEvents="none" children={<Search2Icon color="gray.600" />} />
    <Input
      ref={ref}
      type="text"
      placeholder="Search..."
      border="1px solid #949494"
      value={input}
      onChange={(e) => onChange(e?.target?.value || "")}
    />
  </InputGroup>
));

const SearchResultsView = ({ input }: { input: string }): JSX.Element => {
  const classification: Classification = useMemo(() => classifySearchTerm(input), [input]);

  if (classification.type === "video") {
    return (
      <ChakraLink as={ReactRouterLink} to={`/videos/${classification.sanitized}`}>
        Video: {classification.sanitized}
      </ChakraLink>
    );
  }

  if (classification.type === "playlist") {
    return (
      <ChakraLink as={ReactRouterLink} to={`/playlists/${classification.sanitized}`}>
        Playlist: {classification.sanitized}
      </ChakraLink>
    );
  }

  return <div>TODO: implement other things</div>;
};

export const Search = () => {
  const [userInput, setuserInput] = useState("");
  const { isOpen, onToggle, onClose } = useDisclosure();
  const focusRef = useRef(null);

  useEffect(() => {
    if (userInput && !isOpen) {
      onToggle();
    }
  }, [userInput]);

  return (
    <Popover initialFocusRef={focusRef} isOpen={isOpen} onClose={onClose} placement="bottom" closeOnBlur={true}>
      <PopoverTrigger>
        <SearchInputGroup input={userInput} onChange={setuserInput} />
      </PopoverTrigger>
      <PopoverContent color="white" bg="blue.800" borderColor="blue.800">
        <PopoverArrow bg="blue.800" />
        <PopoverBody>
          <SearchInputGroup ref={focusRef} input={userInput} onChange={setuserInput} />
          <SearchResultsView input={userInput} />
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
};

export default Search;
