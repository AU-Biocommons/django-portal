// Site search UI

const searchElementId = 'search';
const searchElement = $(`#${searchElementId}`);
const searchInput = $(`#${searchElementId} input`);
searchElement.css('display', 'flex');
searchElement.hide();

const showSearch = () => {
    searchElement.fadeIn(250);
    searchInput.focus();

}
const closeSearch = () => {
    searchElement.fadeOut(250);
    searchInput.val('');
}

searchInput.on('keyup', (e) => {
    if (e.keyCode === 27) {
        closeSearch();
    }
    if (e.keyCode === 13) {
        searchElement.find('form').submit();
    }
});

searchElement.find('.backdrop').click( (e) => closeSearch() );
