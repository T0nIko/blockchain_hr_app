pragma solidity ^0.4.21;

contract Reviews {
    address public reviewer;
    address public target;
    string  public review_text;

    function Reviews(address _reviewer, address _target, string data) {
        reviewer = _reviewer;
        target = _target;
        review_text = data;
    }

    function get_review_text() constant returns (string) {
        return review_text;
    }

    function get_review_sender() constant returns (address) {
        return reviewer;
    }

    function get_review_target() constant returns (address) {
        return target;
    }
}
